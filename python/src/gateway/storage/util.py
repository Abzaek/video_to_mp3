import pika, json

def upload(file, grid_fs, channel, access):
    try:
        # Store the file in GridFS
        file_id = grid_fs.put(file, filename=file.filename)
    except Exception as e:
        return 'Internal server error', 500
    
    try:
        # prepare the message to be sent to RabbitMQ
        message = {
            'file_id': str(file_id),
            'mp3_file_id': None, # Placeholder for mp3 file ID
            'filename': file.filename,
            'user_name': access['username']
        }

        message_json = json.dumps(message)

        channel.basic_publish(
            exchange='',
            routing_key='video_upload',
            body=message_json,
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )
    except Exception as e:
        grid_fs.delete(file_id)  # Clean up the file if RabbitMQ fails
        return 'Internal server error', 500


