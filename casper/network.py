"""The network module contains a network class allowing for message passing """
from casper.blockchain.blockchain_protocol import BlockchainProtocol


class Network(object):
    """Simulates a network that allows for message passing between validators."""
    def __init__(self, validator_set, protocol=BlockchainProtocol):
        self.validator_set = validator_set
        if protocol == BlockchainProtocol:
            self.global_view = protocol.View(set(), self.validator_set.genesis_block)
        else:
            self.global_view = protocol.View(set())

    def propagate_message_to_validator(self, message, validator):
        """Propagate a message to a validator."""
        assert message.hash in self.global_view.justified_messages, (
            "...expected only to propagate messages "
            "from the global view")
        assert validator in self.validator_set, "...expected a known validator"

        validator.receive_messages(set([message]))

    def get_message_from_validator(self, validator):
        """Get a message from a validator."""
        assert validator in self.validator_set, "...expected a known validator"

        new_message = validator.make_new_message()
        self.global_view.add_messages(set([new_message]))

        return new_message

    def view_initialization(self, view):
        """Initalizes all validators with all messages in some view."""
        messages = view.justified_messages.values()

        self.global_view.add_messages(messages)

        for validator in self.validator_set:
            validator.receive_messages(messages)

    def random_initialization(self):
        """Generates starting messages for all validators with None as an estimate."""
        for validator in self.validator_set:
            self.get_message_from_validator(validator)
