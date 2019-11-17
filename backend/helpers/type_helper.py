from backend.models.trainer import Trainer


def is_trainer(id):
    if (Trainer.find_by_uuid(id)):
        return True
    else:
        return False


from backend.models.conversation import Conversation


def does_conversation_exist(user_uuid, trainer_uuid):
    user_conversation = Conversation.get_user_by_user_uuid(user_uuid)
    trainer_conversation = Conversation.get_by_trainer_uuid(trainer_uuid)
    print(user_conversation)
    print(trainer_conversation)
    return user_conversation is not None and trainer_conversation is not None

def get_existing_conversation(user_uuid, trainer_uuid):
    user_conversation = Conversation.get_user_by_user_uuid(user_uuid)
    trainer_conversation = Conversation.get_by_trainer_uuid(trainer_uuid)
    if user_conversation is trainer_conversation:
        return user_conversation