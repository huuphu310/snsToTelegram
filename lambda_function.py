def lambda_handler(event, context):
    url = 'https://api.telegram.org/bot%s/sendMessage' % os.environ['TOKEN']
    message = event['Records'][0]['Sns']['Message']
    chunks = wrap(message, MAX_CHUNK_SIZE)

    for chunk in chunks:
        data = parse.urlencode({'chat_id': os.environ['CHAT_ID'], 'text': chunk})
        try:
            # Send the SNS message chunk to Telegram
            request.urlopen(url, data.encode('utf-8'))

        except error.HTTPError as e:
            print('Failed to send the SNS message below:\n%s' % chunk)
            response = json.load(e)
            if 'description' in response:
                print(response['description'])
            raise e
