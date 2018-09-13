from lex.fluent.slot import Slot
s = Slot().with_name('testslot').get()
print(s.name)
