from decimal import Decimal
from operator import itemgetter

from rest_framework import mixins, viewsets
from rest_framework import permissions, status
from rest_framework.response import Response

from countries.models import CountrySettings
from events.models import Ticket
from orders.models import Order, OrderTicket, ORDER_STATUSES
from orders.serializers import OrderCreateSerializer, OrderSerializer
from utils.validation import validate_country


class OrderViewset(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet
):
    queryset = Order.objects.all()
    lookup_field = 'identifier'
    pagination_class = None
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer

        return OrderSerializer

    def create(self, request, *args, **kwargs):
        self.request.data['user'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        ticket_qs = Ticket.objects.with_availability()

        tickets_not_found = []
        tickets_with_lower_availability = []

        order_tickets = data.pop('order_tickets')

        # Validate country and get country settings
        country = self.kwargs['country_country']

        validate_country(country)
        country_settings = CountrySettings.objects.get(country=country)

        tickets_subtotal = Decimal('0')
        service_charge_subtotal = Decimal('0')
        order_total = Decimal('0')

        for index, ticket_data in enumerate(order_tickets):
            ticket_identifier, quantity = itemgetter('ticket_identifier', 'quantity')(ticket_data)

            try:
                ticket = ticket_qs.get(identifier=ticket_identifier)

                if ticket.available_quantity < quantity:
                    tickets_with_lower_availability.append({
                        ticket_identifier: ticket.available_quantity
                    })

                order_tickets[index]['id'] = ticket.id
                order_tickets[index]['price'] = ticket.price
                order_tickets[index]['cost'] = ticket.cost
                order_tickets[index]['subtotal'] = ticket.price * quantity
                order_tickets[index]['service_charge_subtotal'] = country_settings.per_ticket_service_charge * quantity

                tickets_subtotal += order_tickets[index]['subtotal']
                service_charge_subtotal += order_tickets[index]['service_charge_subtotal']
                order_total += tickets_subtotal + service_charge_subtotal

            except Ticket.DoesNotExist:
                tickets_not_found.append(ticket_data['ticket_identifier'])

        if (len(tickets_not_found) > 0 or len(tickets_with_lower_availability) > 0):
            return Response({
                'tickets_not_found': tickets_not_found,
                'tickets_with_lower_availability': tickets_with_lower_availability
            }, status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(
            user=request.user, status=ORDER_STATUSES['IN_PROGRESS'], country=country,
            per_ticket_service_charge=country_settings.per_ticket_service_charge,
            ticket_price_surcharge_percentage=country_settings.ticket_price_surcharge_percentage,
            tickets_subtotal=tickets_subtotal,
            service_charge_subtotal=service_charge_subtotal,
            total=order_total
        )

        for ticket_data in order_tickets:
            OrderTicket.objects.create(
                order=order,
                ticket_id=ticket_data['id'],
                quantity=ticket_data['quantity'],
                price=ticket_data['price'],
                cost=ticket_data['cost'],
                service_charge_subtotal=ticket_data['service_charge_subtotal'],
                subtotal=ticket_data['subtotal']
            )

        serializer = OrderSerializer(order)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # def validate(self, data):
    #     ticket_qs = Ticket.objects.with_availability()

    #     target_tickets = ticket_qs.filter(identifier__in=map(lambda t: t['ticket_identifier'], data['order_tickets']))

    #     if (len(target_tickets) !== len(data['order_tickets')]):
    #         # Some ticket could not be found or is unavailable
    #         raise serializer.ValidationError()

    #     return super().create(request, *args, **kwargs)