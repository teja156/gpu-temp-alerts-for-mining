from discord_webhooks import DiscordWebhooks
import pytz
from datetime import datetime

# Webhook URL for your Discord channel.
WEBHOOK_URL = 'https://discord.com/api/webhooks/856809625692143617/AYlR9hGNe8O5IDOmBPieLzBlWydFGMPT9mTx7GAcNLd1XPOA1fMWUq2RHE3rU4L8vbZF'




def sendMessage(lastSent, content):
	webhook = DiscordWebhooks(WEBHOOK_URL)
	tz = pytz.timezone("Asia/Kolkata")
	timestamp = datetime.now(tz)
	# date_time = datetime.fromtimestamp(timestamp)
	date_time = timestamp.strftime("%d %B, %Y %H:%M:%S")

	
	webhook.add_field(name="Timestamp", value=date_time)
	alert=False

	for i in content:
		# Check if status is Attention or Critical
		if i["Status"] == "Attention" or i["Status"]=="Critical":
			# Send notif immediately
			webhook.set_content(title="ALERT - %s"%i["Status"] , description="You need to take actions now, your GPU temps are not in a recommended state")
			webhook.add_field(name="GPU", value=i["Name"])
			webhook.add_field(name="Temp", value=i["Temp"])
			alert= True


	if alert:
		webhook.send()
		print("Sent Alert")
		return 1

	return 0




