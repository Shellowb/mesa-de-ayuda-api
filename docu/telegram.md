# Telegram

## Response
Responses on telegram are made by a json object called [Update][9], this object can contains diferent sub object, depending on the interaction being made.

This object represents an incoming update.
At most one of the optional parameters can be present in any given update.

### Update [ref][9]

| Field | Type | Description |
| --- | --- | --- |
| update_id | Integer | The update's unique identifier. Update identifiers start from a certain positive number and increase sequentially. This ID becomes especially handy if you're using [Webhooks](#setwebhook), since it allows you to ignore repeated updates or to restore the correct update sequence, should they get out of order. If there are no new updates for at least a week, then identifier of the next update will be chosen randomly instead of sequentially. |
| message | [Message](#message) | _Optional_. New incoming message of any kind — text, photo, sticker, etc. |
| edited_message | [Message](#message) | _Optional_. New version of a message that is known to the bot and was edited |
| channel_post | [Message](#message) | _Optional_. New incoming channel post of any kind — text, photo, sticker, etc. |
| edited\_channel\_post | [Message](#message) | _Optional_. New version of a channel post that is known to the bot and was edited |
| inline_query | [InlineQuery](#inlinequery) | _Optional_. New incoming [inline](#inline-mode) query |
| chosen\_inline\_result | [ChosenInlineResult](#choseninlineresult) | _Optional_. The result of an [inline](#inline-mode) query that was chosen by a user and sent to their chat partner. Please see our documentation on the [feedback collecting](/bots/inline#collecting-feedback) for details on how to enable these updates for your bot. |
| callback_query | [CallbackQuery](#callbackquery) | _Optional_. New incoming callback query |
| shipping_query | [ShippingQuery](#shippingquery) | _Optional_. New incoming shipping query. Only for invoices with flexible price |
| pre\_checkout\_query | [PreCheckoutQuery](#precheckoutquery) | _Optional_. New incoming pre-checkout query. Contains full information about checkout |
| poll | [Poll](#poll) | _Optional_. New poll state. Bots receive only updates about stopped polls and polls, which are sent by the bot |
| poll_answer | [PollAnswer](#pollanswer) | _Optional_. A user changed their answer in a non-anonymous poll. Bots receive new votes only in polls that were sent by the bot itself. |
| my\_chat\_member | [ChatMemberUpdated](#chatmemberupdated) | _Optional_. The bot's chat member status was updated in a chat. For private chats, this update is received only when the bot is blocked or unblocked by the user. |
| chat_member | [ChatMemberUpdated](#chatmemberupdated) | _Optional_. A chat member's status was updated in a chat. The bot must be an administrator in the chat and must explicitly specify “chat_member” in the list of _allowed_updates_ to receive these updates. |
| chat\_join\_request | [ChatJoinRequest](#chatjoinrequest) | _Optional_. A request to join the chat has been sent. The bot must have the _can\_invite\_users_ administrator right in the chat to receive these updates. |

### Message [ref][10]

| Field | Type | Description |
| --- | --- | --- |
| message_id | Integer | Unique message identifier inside this chat |
| from | [User](#user) | _Optional_. Sender of the message; empty for messages sent to channels. For backward compatibility, the field contains a fake sender user in non-channel chats, if the message was sent on behalf of a chat. |
| sender_chat | [Chat](#chat) | _Optional_. Sender of the message, sent on behalf of a chat. For example, the channel itself for channel posts, the supergroup itself for messages from anonymous group administrators, the linked channel for messages automatically forwarded to the discussion group. For backward compatibility, the field _from_ contains a fake sender user in non-channel chats, if the message was sent on behalf of a chat. |
| date | Integer | Date the message was sent in Unix time |
| chat | [Chat](#chat) | Conversation the message belongs to |
| forward_from | [User](#user) | _Optional_. For forwarded messages, sender of the original message |
| forward\_from\_chat | [Chat](#chat) | _Optional_. For messages forwarded from channels or from anonymous administrators, information about the original sender chat |
| forward\_from\_message_id | Integer | _Optional_. For messages forwarded from channels, identifier of the original message in the channel |
| forward_signature | String | _Optional_. For forwarded messages that were originally sent in channels or by an anonymous chat administrator, signature of the message sender if present |
| forward\_sender\_name | String | _Optional_. Sender's name for messages forwarded from users who disallow adding a link to their account in forwarded messages |
| forward_date | Integer | _Optional_. For forwarded messages, date the original message was sent in Unix time |
| is\_automatic\_forward | True | _Optional_. True, if the message is a channel post that was automatically forwarded to the connected discussion group |
| reply\_to\_message | [Message](#message) | _Optional_. For replies, the original message. Note that the Message object in this field will not contain further _reply\_to\_message_ fields even if it itself is a reply. |
| via_bot | [User](#user) | _Optional_. Bot through which the message was sent |
| edit_date | Integer | _Optional_. Date the message was last edited in Unix time |
| has\_protected\_content | True | _Optional_. True, if the message can't be forwarded |
| media\_group\_id | String | _Optional_. The unique identifier of a media message group this message belongs to |
| author_signature | String | _Optional_. Signature of the post author for messages in channels, or the custom title of an anonymous group administrator |
| text | String | _Optional_. For text messages, the actual UTF-8 text of the message, 0-4096 characters |
| entities | Array of [MessageEntity](#messageentity) | _Optional_. For text messages, special entities like usernames, URLs, bot commands, etc. that appear in the text |
| animation | [Animation](#animation) | _Optional_. Message is an animation, information about the animation. For backward compatibility, when this field is set, the _document_ field will also be set |
| audio | [Audio](#audio) | _Optional_. Message is an audio file, information about the file |
| document | [Document](#document) | _Optional_. Message is a general file, information about the file |
| photo | Array of [PhotoSize](#photosize) | _Optional_. Message is a photo, available sizes of the photo |
| sticker | [Sticker](#sticker) | _Optional_. Message is a sticker, information about the sticker |
| video | [Video](#video) | _Optional_. Message is a video, information about the video |
| video_note | [VideoNote](#videonote) | _Optional_. Message is a [video note](https://telegram.org/blog/video-messages-and-telescope), information about the video message |
| voice | [Voice](#voice) | _Optional_. Message is a voice message, information about the file |
| caption | String | _Optional_. Caption for the animation, audio, document, photo, video or voice, 0-1024 characters |
| caption_entities | Array of [MessageEntity](#messageentity) | _Optional_. For messages with a caption, special entities like usernames, URLs, bot commands, etc. that appear in the caption |
| contact | [Contact](#contact) | _Optional_. Message is a shared contact, information about the contact |
| dice | [Dice](#dice) | _Optional_. Message is a dice with random value |
| game | [Game](#game) | _Optional_. Message is a game, information about the game. [More about games »](#games) |
| poll | [Poll](#poll) | _Optional_. Message is a native poll, information about the poll |
| venue | [Venue](#venue) | _Optional_. Message is a venue, information about the venue. For backward compatibility, when this field is set, the _location_ field will also be set |
| location | [Location](#location) | _Optional_. Message is a shared location, information about the location |
| new\_chat\_members | Array of [User](#user) | _Optional_. New members that were added to the group or supergroup and information about them (the bot itself may be one of these members) |
| left\_chat\_member | [User](#user) | _Optional_. A member was removed from the group, information about them (this member may be the bot itself) |
| new\_chat\_title | String | _Optional_. A chat title was changed to this value |
| new\_chat\_photo | Array of [PhotoSize](#photosize) | _Optional_. A chat photo was change to this value |
| delete\_chat\_photo | True | _Optional_. Service message: the chat photo was deleted |
| group\_chat\_created | True | _Optional_. Service message: the group has been created |
| supergroup\_chat\_created | True | _Optional_. Service message: the supergroup has been created. This field can't be received in a message coming through updates, because bot can't be a member of a supergroup when it is created. It can only be found in reply\_to\_message if someone replies to a very first message in a directly created supergroup. |
| channel\_chat\_created | True | _Optional_. Service message: the channel has been created. This field can't be received in a message coming through updates, because bot can't be a member of a channel when it is created. It can only be found in reply\_to\_message if someone replies to a very first message in a channel. |
| message\_auto\_delete\_timer\_changed | [MessageAutoDeleteTimerChanged](#messageautodeletetimerchanged) | _Optional_. Service message: auto-delete timer settings changed in the chat |
| migrate\_to\_chat_id | Integer | _Optional_. The group has been migrated to a supergroup with the specified identifier. This number may have more than 32 significant bits and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a signed 64-bit integer or double-precision float type are safe for storing this identifier. |
| migrate\_from\_chat_id | Integer | _Optional_. The supergroup has been migrated from a group with the specified identifier. This number may have more than 32 significant bits and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a signed 64-bit integer or double-precision float type are safe for storing this identifier. |
| pinned_message | [Message](#message) | _Optional_. Specified message was pinned. Note that the Message object in this field will not contain further _reply\_to\_message_ fields even if it is itself a reply. |
| invoice | [Invoice](#invoice) | _Optional_. Message is an invoice for a [payment](#payments), information about the invoice. [More about payments »](#payments) |
| successful_payment | [SuccessfulPayment](#successfulpayment) | _Optional_. Message is a service message about a successful payment, information about the payment. [More about payments »](#payments) |
| connected_website | String | _Optional_. The domain name of the website on which the user has logged in. [More about Telegram Login »](/widgets/login) |
| passport_data | [PassportData](#passportdata) | _Optional_. Telegram Passport data |
| proximity\_alert\_triggered | [ProximityAlertTriggered](#proximityalerttriggered) | _Optional_. Service message. A user in the chat triggered another user's proximity alert while sharing Live Location. |
| voice\_chat\_scheduled | [VoiceChatScheduled](#voicechatscheduled) | _Optional_. Service message: voice chat scheduled |
| voice\_chat\_started | [VoiceChatStarted](#voicechatstarted) | _Optional_. Service message: voice chat started |
| voice\_chat\_ended | [VoiceChatEnded](#voicechatended) | _Optional_. Service message: voice chat ended |
| voice\_chat\_participants_invited | [VoiceChatParticipantsInvited](#voicechatparticipantsinvited) | _Optional_. Service message: new participants invited to a voice chat |
| reply_markup | [InlineKeyboardMarkup](#inlinekeyboardmarkup) | _Optional_. Inline keyboard attached to the message. `login_url` buttons are represented as ordinary `url` buttons. |


### CallBack Query [ref][11]
| Field | Type | Description |
| --- | --- | --- |
| id  | String | Unique identifier for this query |
| from | [User](#user) | Sender |
| message | [Message](#message) | _Optional_. Message with the callback button that originated the query. Note that message content and message date will not be available if the message is too old |
| inline\_message\_id | String | _Optional_. Identifier of the message sent via the bot in inline mode, that originated the query. |
| chat_instance | String | Global identifier, uniquely corresponding to the chat to which the message with the callback button was sent. Useful for high scores in [games](#games). |
| data | String | _Optional_. Data associated with the callback button. Be aware that a bad client can send arbitrary data in this field. |
| game\_short\_name | String | _Optional_. Short name of a [Game](#games) to be returned, serves as the unique identifier for the game |

### Keyboard message API Request example
> Al enviar un mensaje a la API, hay ciertos casos, en que si el JSON no es válido la API muestra un mensaje de error en la respuesta, pero por alguna razón no siempre se recibe en el post, sino que llega como un get. Por lo tanto el get se puede usar para atrapar o leer ciertos errores. --> RE checkar.
> It's very important not pretify the jsons. python function json dumps as example do not works well in telegram API for example
    ```python
    json.dumps(
          {
            "inline_keyboard":
                [[
                    {"text": "Si", "url": "https://core.telegram.org/bots"},
                    {"text": "No", "url": "https://core.telegram.org/bots"}
                ]]
          }
        )
      )
    # will return :
    {'ok': False, 'error_code': 400, 'description': "Bad Request: can't parse reply keyboard markup JSON object"} 
    # <Response [400]>

    #Instead
    json.dumps(
          {
            "inline_keyboard":
                [[
                    {"text": "Si", "url": "https://core.telegram.org/bots"},
                    {"text": "No", "url": "https://core.telegram.org/bots"}
                ]]
          }
        , separators=(',', ':'))
      )
    # will return:
    {'ok': True, 'result': {'message_id': 845, 'from': {'id': 1231231235, 'is_bot': True, 'first_name': 'mesadeayuda_dev', 'username': 'mesadeayuda_dev_bot'}, 'chat': {'id': 1231123, 'first_name': 'Shellow', 'username': 'Shellowb', 'type': 'private'}, 'date': 12566431, 'text': 'Recuerda que puedes obtener mas información sobre la mesa de ayuda DCC en mesadeayuda.cl En caso de no poder contestar tu consulta, puedo contactar a un /asistente por este mismo canal', 'entities': [{'offset': 0, 'length': 74, 'type': 'italic'}, {'offset': 74, 'length': 14, 'type': 'text_link', 'url': 'https://mesadeayuda.cadcc.cl/'}, {'offset': 74, 'length': 14, 'type': 'italic'}, {'offset': 89, 'length': 64, 'type': 'italic'}, {'offset': 153, 'length': 10, 'type': 'bot_command'}, {'offset': 153, 'length': 10, 'type': 'italic'}, {'offset': 164, 'length': 20, 'type': 'italic'}], 'reply_markup': {'inline_keyboard': [[{'text': 'Si', 'url': 'https://core.telegram.org/bots'}, {'text': 'No', 'url': 'https://core.telegram.org/bots'}]]}}} 
    # <Response [200]>
    ```

`https://api.telegram.org/bot1914846977:AAGW_BXn_ia8zECT5laArhrgIZEFXk3Yb1M/sendMessage`

_Keyboard_

```json
{
    "chat_id": 187579960,
    "text": "message",
    "parse_mode": "MarkdownV2",
    "reply_markup": 
        {
            "keyboard":
                [[
                    {"text": "Si"},
                    {"text": "No"}
                ]]
        }
}
```
_Inline_keyboard_

```json
{
    "chat_id": 187579960,
    "text": "message",
    "parse_mode": "MarkdownV2",
    "reply_markup": 
        {
            "inline_keyboard":
                [[
                    {"text": "Si", "url": "https://core.telegram.org/bots"},
                    {"text": "No", "url": "https://core.telegram.org/bots"}
                ]]
        }
}
```

python full example
```python
def send_message(message, chat_id, keyboard_button={}):
    data = {
      "chat_id": chat_id,
      "text": message,
      "parse_mode": "MarkdownV2",
      "reply_markup": (None,
        json.dumps(
          {
            "inline_keyboard":
                [[
                    {"text": "Si", "url": "https://core.telegram.org/bots"},
                    {"text": "No", "url": "https://core.telegram.org/bots"}
                ]]
          }
        , separators=(',', ':'))
      )
    }
    response = requests.post(
      f"{env('TELEGRAM_URL')}{env('BOT_TOKEN')}/sendMessage", data=data
    )    
    print(response.json(), response)
```



## Referencias
[0]: https://core.telegram.org/bots
[1]: https://core.telegram.org/bots/api
[2]: https://core.telegram.org/schema
[3]: https://github.com/python-telegram-bot
[4]: https://github.com/python-telegram-bot/python-telegram-bot/wiki/
[5]: https://python-telegram-bot.readthedocs.io/en/stable/
[6]: https://core.telegram.org/bots/api#sendmessage
[7]: https://core.telegram.org/bots/inline
[8]: https://github.com/python-telegram-bot/python-telegram-bot/wiki/Introduction-to-the-API
[9]: https://core.telegram.org/bots/api#update
[10]: https://core.telegram.org/bots/api#message
[11]: https://core.telegram.org/bots/api#callbackquery