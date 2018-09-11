from lex.fluent.slot import Slot
from lex.fluent.intent import Intent

s = Slot(Name='testslot').with_value('AMAZON.NUMBER').apply()
s = Slot(Name='test_timeslot').with_value('AMAZON.NUMBER').apply()
i = Intent(Name='test_intent').with_slot(s).apply()
