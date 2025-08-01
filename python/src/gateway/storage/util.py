import pika, json, logging

def upload(file, grid_fs, channel, access):
    try:
        # Store the file in GridFS
        file_id = grid_fs.put(file, filename=file.filename)
    except Exception as e:
        logging.error(f"Error storing file in GridFS: {e}")
        return 'Internal server error', 500
    
    logging.info(f"File stored in GridFS with ID: {file_id} for user: {access}")

    try:
        # prepare the message to be sent to RabbitMQ
        message = {
            'video_fid': str(file_id),
            'mp3_fid': None, # Placeholder for mp3 file ID
            'filename': file.filename,
            'user_name': access['username']
        }

        message_json = json.dumps(message)

        channel.basic_publish(
            exchange='',
            routing_key='video',
            body=message_json,
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )
    except Exception as e:
        logging.error(f"Error publishing message to RabbitMQ: {e}")
        grid_fs.delete(file_id)  # Clean up the file if RabbitMQ fails
        return 'Internal server error', 500


