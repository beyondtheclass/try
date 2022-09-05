
from flask import Flask, render_template,request
import logging
import json

# pip install heyoo

from heyoo import WhatsApp

application = Flask(__name__)

Token = 'EAAIywjAqIe8BAMrUXJmeZCE3cVWM80mYkbmLeHiuNZCXqFJaVBvBgfhNuSuqbK48kxRIxhLDlx4sxEZBajhsMNxeDRty0ne3qfYZAjtlpN8FW0qFtgQkEXjEJlUjYa9Oxwu3ICdSasU6Xekj77ZByXp3ZA7xN5tcZB59mDkxPgw622DJ8ZAHr7PBmBEHjbyvpIwTNkLqi1c2vel8htUQRXXH'
messenger = WhatsApp(Token, phone_number_id='106592595452225')


VERIFY_TOKEN = "30cca545-3838-48b2-80a7-9e43b1ae8ce4"


# application.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{username}:{password}@{host}:{port}/{database}'.format(
#         username='flask-movies',
#         password='complexpassword123',
#         host='localhost',
#         port='5432',
#         database='flask-movies',
#     )


@application.route('/',methods=['GET','POST'])
def heyoo():

    print(request.headers)

    # complicated
    if request.method == "GET":
        if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
            if not request.args.get("hub.verify_token") == VERIFY_TOKEN:
                return "Verification token mismatch", 403
            return request.args["hub.challenge"], 200


  # Handle Webhook Subscriptions
    data = request.get_json()
    logging.info("Received webhook data: %s", data)
    changed_field = messenger.changed_field(data)

    if changed_field == "messages":
        new_message = messenger.get_mobile(data)
        if new_message:
            mobile = messenger.get_mobile(data)
            name = messenger.get_name(data)
            message_type = messenger.get_message_type(data)
            logging.info(
                f"New Message; sender:{mobile} name:{name} type:{message_type}"
            )
            if message_type == "text":
                message = messenger.get_message(data)
                name = messenger.get_name(data)
                logging.info("Message: %s", message)
                # messenger.send_message(f"Hi {name}, nice to connect with you", mobile)


                # messenger.send_image(recipient_id=mobile, image='https://cataas.com/cat', caption="try")

               

                # here
                # messenger.send_button(
                #     recipient_id=mobile,
                #     button={
                #         "header": " Header ",
                #         "body": "Awesome i found the following payment profiles associated with your number *** *** 330. Please choose your preferd payment method",
                #         "footer": " Header ",
                #         "action": {

                #             "button": "Pay now",
                #             "sections": [
                #                 {
                #                     "title": "options",
                #                     "rows": [
                #                         {"id": "row 1", "title": "Yes,  I'll be there", "description": ""},

                #                         {
                #                             "id": "row 2", "title": "Sorry, can't make it", "description": "",
                #                         },
                #                     ],
                #                 }
                #             ],
                #         },
                #     },
                # )
                # here

                messenger.send_reply_button(
                        recipient_id=mobile,
                        button={
                            "type": "button",

                            "body": {
                                "text": f"Hey {name}! welcome to Nopa quick checkout experience on WhatsApp."
                            },
                            "action": {
                                "buttons": [
                                    {
                                        "type": "reply",
                                        "reply": {
                                            "id": "b1",
                                            "title": "Checkout"
                                        }
                                    },
                                    # {
                                    #     "type": "reply",
                                    #     "reply": {
                                    #         "id": "b2",
                                    #         "title": "Send activation link"
                                    #     }
                                    # }
                                ]
                            }
                      },
                    )
                # here


            elif message_type == "interactive":
                message_response = messenger.get_interactive_response(data)
                intractive_type = message_response.get("type")
                message_id = message_response[intractive_type]["id"]
                message_text = message_response[intractive_type]["title"]
                logging.info(f"Interactive Message; {message_id}: {message_text}")

                if message_id == "b1":
                    messenger.send_message(f"Hi {name}, kindly 📍share your shipping location.", mobile)
                if message_id == "b2":
                    messenger.send_message(f"Hi {name}, Please share your M-pesa payment number", mobile)
                if message_id == "b3":
                    messenger.send_document(document='http://www.africau.edu/images/default/sample.pdf', recipient_id=mobile, caption="e-receipt")
                    messenger.send_message("Thank you for completing your order! if you want to track your delivery, send me the order number 😊", mobile)


                    

            elif message_type == "location":
                message_location = messenger.get_location(data)
                message_latitude = message_location["latitude"]
                message_longitude = message_location["longitude"]
                logging.info("Location: %s, %s", message_latitude, message_longitude)


                messenger.send_reply_button(
                        recipient_id=mobile,
                        button={
                            "type": "button",

                            "body": {
                                "text": f"Easy, secure and convenient way to make payments with your number *** *** 330"
                            },
                            "action": {
                                "buttons": [
                                    {
                                        "type": "reply",
                                        "reply": {
                                            "id": "b3",
                                            "title": "Lipa na M-pesa"
                                        }
                                    },
                                    {
                                        "type": "reply",
                                        "reply": {
                                            "id": "b2",
                                            "title": "Change number"
                                        }
                                    }
                                ]
                            }
                      },
                    )

                
            elif message_type == "image":
                image = messenger.get_image(data)
                image_id, mime_type = image["id"], image["mime_type"]
                image_url = messenger.query_media_url(image_id)
                image_filename = messenger.download_media(image_url, mime_type)
                print(f"{mobile} sent image {image_filename}")

                # media_id = messenger.upload_media(
                #             media='path/to/media',
                #         )['id']
                
                # messenger.send_image(
                #         image=media_id,
                #         recipient_id="mobile",
                #         link=False
                #     )



                logging.info(f"{mobile} sent image {image_filename}")

            elif message_type == "video":
                video = messenger.get_video(data)
                video_id, mime_type = video["id"], video["mime_type"]
                video_url = messenger.query_media_url(video_id)
                video_filename = messenger.download_media(video_url, mime_type)
                print(f"{mobile} sent video {video_filename}")
                logging.info(f"{mobile} sent video {video_filename}")

            elif message_type == "audio":
                audio = messenger.get_audio(data)
                audio_id, mime_type = audio["id"], audio["mime_type"]
                audio_url = messenger.query_media_url(audio_id)
                audio_filename = messenger.download_media(audio_url, mime_type)
                print(f"{mobile} sent audio {audio_filename}")
                logging.info(f"{mobile} sent audio {audio_filename}")

            elif message_type == "file":
                file = messenger.get_file(data)
                file_id, mime_type = file["id"], file["mime_type"]
                file_url = messenger.query_media_url(file_id)
                file_filename = messenger.download_media(file_url, mime_type)
                print(f"{mobile} sent file {file_filename}")
                logging.info(f"{mobile} sent file {file_filename}")
            else:
                print(f"{mobile} sent {message_type} ")
                print(data)
        else:
            delivery = messenger.get_delivery(data)
            if delivery:
                print(f"Message : {delivery}")
            else:
                print("No new message")
    return "ok"


@application.route("/map")
def map():
    return render_template("map.html")


@application.route("/try")
def trys():
    return render_template("try.html")


@application.route("/about")
def about():
    return render_template("about.html")

@application.route("/martime_education")
def martime_education():
    return render_template("maritime_education.html")

@application.route("/free_trade")
def free_trade():
    return render_template("free_trade.html")

@application.route("/grid")
def grid():
    return render_template("grid.html")

if __name__ == "__main__":
    application.debug=True
    application.run()
