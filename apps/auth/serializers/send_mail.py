from rest_framework import serializers
class SendMailInputSerializer(serializers.Serializer):
    template_id = serializers.IntegerField()
    subject = serializers.CharField(max_length=255)
    mail_to = serializers.ListField(
        child=serializers.EmailField(),
        allow_empty=False,
        required=True
    )
    mail_cc = serializers.ListField(
        child=serializers.EmailField(required=False),
        required=False,
        allow_empty=True
    )
    body = serializers.DictField(required=False)