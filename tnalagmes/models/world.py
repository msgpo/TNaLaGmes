#!/usr/bin/python
from datetime import date
from datetime import timedelta
from datetime import datetime
import random
from tnalagmes import TNaLaGmesConstruct
from tnalagmes.models.objects import Inventory


class Scene(TNaLaGmesConstruct):
    """
    go up / down / left / right / front /back
    go north / south / west / east ....
    who is in the roon
    items in the room
    connected rooms
    describe room
    room name
    """
    def __init__(self, name, description="empty room", items=None, npcs=None, directions=None):
        TNaLaGmesConstruct.__init__(self, "room")
        self.name = name
        self.description = description
        self.items = items or Inventory()
        self.npcs = npcs or {}
        self.connections = directions or {}

    def add_connection(self, room, direction="front", message=None):
        if isinstance(room, str):
            room = Scene(room)
        self.connections[direction] = room
        message = message or direction + " there is a " + room.name
        self.description += "\n" + message

    def handle_up(self, intent):
        return ""

    def handle_down(self, intent):
        return ""

    def handle_front(self, intent):
        return ""

    def handle_back(self, intent):
        return ""

    def handle_left(self, intent):
        return ""

    def handle_right(self, intent):
        return ""

    def handle_north(self, intent):
        return ""

    def handle_south(self, intent):
        return ""

    def handle_east(self, intent):
        return ""

    def handle_west(self, intent):
        return ""

    def handle_northeast(self, intent):
        return ""

    def handle_northwest(self, intent):
        return ""

    def handle_southeast(self, intent):
        return ""

    def handle_southweast(self, intent):
        return ""

    def handle_describe(self, intent):
        return self.description

    def handle_look(self, intent):
        item = intent.get("item", "room")
        if item == "room":
            return self.handle_describe(intent)
        return "it is a " + item

    def handle_get(self, intent):
        item = intent.get("item", "nothing")
        if item in self.items:
            item = self.items[item].name
        return "got " + item

    def handle_talk(self, intent):
        npc = intent.get("npc", "yourself")
        if npc in self.npcs:
            npc = self.npcs[npc].name
        return self.talk_to_npc(npc)

    def register_default_intents(self):
        self.register_intent("up", ["up"], self.handle_up)
        self.register_intent("down", ["down"], self.handle_down)
        self.register_intent("front", ["forward"], self.handle_front)
        self.register_intent("back", ["back", "backward"], self.handle_back)
        self.register_intent("left", ["left"], self.handle_left)
        self.register_intent("right", ["right"], self.handle_right)
        self.register_intent("north", ["north"], self.handle_north)
        self.register_intent("south", ["south"], self.handle_south)
        self.register_intent("east", ["east"], self.handle_east)
        self.register_intent("west", ["west"], self.handle_west)
        self.register_intent("northeast", ["northeast"], self.handle_northeast)
        self.register_intent("northwest", ["northwest"], self.handle_northwest)
        self.register_intent("southeast", ["southeast"], self.handle_southeast)
        self.register_intent("southwest", ["southwest"], self.handle_southweast)
        self.register_intent("describe", ["describe room", "describe surroundings", "look"], self.handle_describe)
        self.register_intent("look", ["look {item}", "look at {item}", "describe {item}"], self.handle_look)
        self.register_intent("get", ["get {item}", "acquire {item}", "fetch {item}", "pick {item}", "stash {item}"], self.handle_look)
        self.register_intent("talk", ["talk with {npc}", "engage {npc}", "interact with {npc}"],
                             self.handle_look)

    def get_item(self, item):
        if item in self.items:
            item = self.items[item]
            self.items.pop(item)
            return item
        return None

    def talk_to_npc(self, npc, utterance="hello"):
        if npc in self.npcs:
            return self.npcs[npc].parse_command(utterance)
        return "talk to who?"


class Player(TNaLaGmesConstruct):
    def __init__(self, health, name="you", mana=0, attack=1, magic=None, inventory=None):
        TNaLaGmesConstruct.__init__(self, "player")
        self.max_hp = health
        self.hp = health
        self.max_mp = mana
        self.mp = mana
        self.attack_low = attack - 20
        self.attack_high = attack + 20
        self.magic = magic or []
        self.items = inventory or Inventory()
        self.actions = ["Attack", "Magic", "Items"]
        self.name = name

    def attack(self):
        return random.randrange(self.attack_low, self.attack_high)

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def heal(self, dmg):
        self.hp += dmg
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def spend_mana(self, cost):
        self.mp -= cost

    def cast_spell(self):
        if not len(self.magic):
            return "", 0
        spell = random.choice(self.magic)
        magic_dmg = spell.attack()

        pct = self.hp / self.max_hp * 100

        if self.mp < spell.cost or spell.type == "white" and pct > 50:
            self.cast_spell()
        else:
            return spell, magic_dmg

    def register_default_intents(self):

        def hello(intent):
            return "hello world"

        self.register_intent("hello", ["hi", "hey", "hello", "how are you", "yo"], hello)
