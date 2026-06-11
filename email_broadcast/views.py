from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views import View

from .models import CampaignRecipient, CampaignLink, Campaign
from .tasks import TRANSPARENT_GIF


class PixelTrackerView(View):
    def get(self, request, token):
        try:
            recipient = CampaignRecipient.objects.select_related('campaign').get(pixel_token=token)
            if not recipient.opened:
                recipient.opened = True
                recipient.opened_at = timezone.now()
                recipient.save(update_fields=['opened', 'opened_at'])
                Campaign.objects.filter(pk=recipient.campaign_id).update(
                    open_count=recipient.campaign.open_count + 1
                )
        except CampaignRecipient.DoesNotExist:
            pass
        return HttpResponse(TRANSPARENT_GIF, content_type='image/gif')


class LinkTrackerView(View):
    def get(self, request, token):
        link = get_object_or_404(CampaignLink, token=token)
        CampaignLink.objects.filter(pk=link.pk).update(click_count=link.click_count + 1)
        Campaign.objects.filter(pk=link.campaign_id).update(
            click_count=link.campaign.click_count + 1
        )
        return HttpResponseRedirect(link.original_url)
