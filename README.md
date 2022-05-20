# to_sr

curl -X POST -H "Content-type: application/json" -d "{\"firstName\" : \"John\"}" "http://127.0.0.1:8443/post_json"![image](https://user-images.githubusercontent.com/52318917/169531424-98618491-2f48-41ae-86bb-7931f896b210.png)


def process_json():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        string_val = request.json
        value=json.load(string_val)
        print(value['firstName'])
        return string_val

    else:
        return 'Content-Type not supported!'
