# to_sr



curl -X POST -H "Content-Type: application/json" -d "{\"callId\" : \"bj28705a-48b8-4160-9a5b-c8acae457923\",\"textToValidate\" :\"If you enroll in a promotional APR, you may see limited plan duration options during the promotional period when you use Plan It on your account\",\"spokenText\":\"All of the other terms and aprs for your account like cash advance APR and penalty APR still apply.If you enroll in a promotional APR you may say limited plan duration options during the promotional period when you use planet on your account?You will not be eligible for this promotional APR if you accepted another promotional APR offer from American Express prior to responding to this offer.Can I answer any questions for you?\"}" http://127.0.0.1:8443/comparison


{"callId":"bj28705a-48b8-4160-9a5b-c8acae457923","confidenceRate":"Read","confidenceScore":83.0,"spokenText":"you enroll in a promotional apr you may say limited plan duration options during the promotional period when you use","validatedText":"If you enroll in a promotional APR, you may see limited plan duration options during the promotional period when you use Plan It on your account"}



***************

curl -X POST -H "Content-Type: application/json" -d "{\"callId\" : \"bj28705a-48b8-4160-9a5b-c8acae457923\",\"textToValidate\" :\"If you enroll in a promotional APR, you may see limited plan duration options during the promotional period when you use Plan It on your account\",\"spokenText\":\"All of the other terms and aprs for your account like cash advance APR and penalty APR still apply.If you enroll in a promotional APR you may say limited plan duration options during the promotional period when you use planet on your account?You will not be eligible for this promotional APR if you accepted another promotional APR offer from American Express prior to responding to this offer.Can I answer any questions for you?\"}" http://127.0.0.1:8443/comparison
{"callId":"bj28705a-48b8-4160-9a5b-c8acae457923","confidenceRate":"Not Read","confidenceScore":16.0,"spokenText":"use planet on your accountyou will not be eligible for this promotional apr if you accepted another promotional apr offer from american express prior to","validatedText":"If you enroll in a promotional APR, you may see limited plan duration options during the promotional period when you use Plan It on your account"}



def process_json():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        string_val = request.json
        value=json.load(string_val)
        print(value['firstName'])
        return string_val

    else:
        return 'Content-Type not supported!'
