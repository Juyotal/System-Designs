import pika, json

def upload(f, fs, channel, access):
    try:
        f_id = fs.put(f)
    except Exception as err:
        return " internal sever error", 500

    message = {
        "video_f_id": str(f_id),
        "mp3_f_id": None,
        "username": access["username"]
    }

    try: 
        channel.basic_publish(
            exchange="",
            routing_key="video",
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode = pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )
    except:
        fs.delete(f_id)
        return "internal server error", 500
        