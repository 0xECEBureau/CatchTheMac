SELECT * FROM Files WHERE fileID LIKE '%sms%' OR domain LIKE '%sms%' OR relativePath LIKE '%sms%';

3d0d7e5fb2ce288813306e4d4636395e047a3d28|HomeDomain|Library/SMS/sms.db|1|bplist00


sqlite3 3d0d7e5fb2ce288813306e4d4636395e047a3d28
SQLite version 3.40.1 2022-12-28 14:03:47
Enter ".help" for usage hints.
sqlite> .tables
_SqliteDatabaseProperties              message
attachment                             message_attachment_join
chat                                   message_processing_task
chat_handle_join                       recoverable_message_part
chat_message_join                      sync_deleted_attachments
chat_recoverable_message_join          sync_deleted_chats
deleted_messages                       sync_deleted_messages
handle                                 unsynced_removed_recoverable_messages
kvtable


sqlite> select * from chat;
1|SMS;-;kristy.friedman@outlook.com|45|3|99EAFB66-6331-445C-80AD-228BC97B5553|bplist00   _*prefersTextResponseToIncomingAudioMessages_hasViewedPotentialSpamChat_CKChatWatermarkMessageID_CKChatWatermarkTime_hasBeenAutoSpamReported               |kristy.friedman@outlook.com|SMS||E:|0|||D14507DA-F2B8-4C85-A3E2-949C0A30497F|1|0|||0|BA04CCB379FE12AE636B13E0702A097DE4B516D9|0|||0|0|0
