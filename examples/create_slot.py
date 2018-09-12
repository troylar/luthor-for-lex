from lex.fluent.slot import Slot
from lex.fluent.intent import Intent, IntentSlot
from lex import LexBotManager, LexIntentManager, LexSlotManager, LexPlayer


s = Slot(Name='testslot').with_value('AMAZON.NUMBER').apply()
s = Slot(Name='test_timeslot').with_description('test_descript').apply()
intslot = IntentSlot(Slot=s)
intslot.with_slot_constraint('Required').with_slot_type('AMAZON.Number')
i = Intent(Name='test_intent').with_slot(intslot).apply()
