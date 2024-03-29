from rest_framework import serializers

from events.serializers import EventBasicSerializer
from homepages.models import Homepage, HomepageSlide


class HomepageSlideSerializer(serializers.ModelSerializer):
    image_large = serializers.ImageField(read_only=True)
    event_slug = serializers.SerializerMethodField()
    organizer_slug = serializers.SerializerMethodField()

    def get_event_slug(self, obj):
        return obj.event.slug if obj.event else None

    def get_organizer_slug(self, obj):
        return obj.organizer.slug if obj.organizer else None

    class Meta:
        model = HomepageSlide
        fields = (
            'order', 'date_text', 'venue_text', 'button_text', 'event_slug',
            'organizer_slug', 'link', 'image_large'
        )


class HomepageDetailSerializer(serializers.ModelSerializer):
    slides = HomepageSlideSerializer(many=True)

    class Meta:
        model = Homepage
        fields = (
            'slides', 'about_us_module_button_text', 'about_us_module_heading',
            'about_us_module_title', 'about_us_module_subtitle', 'about_us_module_text',
            'about_us_module_button_text', 'contact_us_module_event_today', 'contact_us_module_text',
            'sell_module_button_text', 'sell_module_text', 'sell_module_title', 'warranty_module_buy_sell_text',
            'warranty_module_customer_service_text', 'warranty_module_warranty_text'
        )
