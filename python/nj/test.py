import os
cwd = os.getcwd()
print("cwd: " +  cwd )
print("ENV:")
for name, value in os.environ.items():
    print("{0}: {1}".format(name, value))
print("ENV_DONE")
import sys
print("print(sys.path): ", sys.path)

import flatbuffers
# main.py
import Example.Person as Person
# import third_party.f.flatbuffers.eval.Example.Person as Person
from MyGame.Sample import Color
from MyGame.Sample import Equipment
from MyGame.Sample import Vec3
from MyGame.Sample import Monster
from MyGame.Sample import Weapon

# from MyGame.Sample.Color import Color
# from MyGame.Sample.Equipment import Equipment
# from MyGame.Sample.Vec3 import Vec3
# from MyGame.Sample.Monster import Monster
# from MyGame.Sample.Weapon import Weapon

# from MyGame.Sample.Color import *
# from MyGame.Sample.Equipment import *
# from MyGame.Sample.Vec3 import *
# from MyGame.Sample.Monster import *
# from MyGame.Sample.Weapon import *


def testMonster():
    # Create a `FlatBufferBuilder`, which will be used to create our
    # monsters' FlatBuffers.
    builder = flatbuffers.Builder(1024)
    weapon_one = builder.CreateString('Sword')
    weapon_two = builder.CreateString('Axe')
    
    # Create the first `Weapon` ('Sword').
    Weapon.Start(builder)
    Weapon.AddName(builder, weapon_one)
    Weapon.AddDamage(builder, 3)
    sword = Weapon.End(builder)
    
    # Create the second `Weapon` ('Axe').
    Weapon.Start(builder)
    Weapon.AddName(builder, weapon_two)
    Weapon.AddDamage(builder, 5)
    axe = Weapon.End(builder)

    # Serialize a name for our monster, called "Orc".
    name = builder.CreateString("Orc")
    
    # Create a `vector` representing the inventory of the Orc. Each number
    # could correspond to an item that can be claimed after he is slain.
    # Note: Since we prepend the bytes, this loop iterates in reverse.
    Monster.StartInventoryVector(builder, 10)
    for i in reversed(range(0, 10)):
        builder.PrependByte(i)
    inv = builder.EndVector()

    # Create a FlatBuffer vector and prepend the weapons.
    # Note: Since we prepend the data, prepend them in reverse order.
    Monster.StartWeaponsVector(builder, 2)
    builder.PrependUOffsetTRelative(axe)
    builder.PrependUOffsetTRelative(sword)
    weapons = builder.EndVector()

    Monster.StartPathVector(builder, 2)
    Vec3.CreateVec3(builder, 1.0, 2.0, 3.0)
    Vec3.CreateVec3(builder, 4.0, 5.0, 6.0)
    path = builder.EndVector()


    # Create our monster by using `Monster.Start()` and `Monster.End()`.
    Monster.Start(builder)
    Monster.AddPos(builder,
                            Vec3.CreateVec3(builder, 1.0, 2.0, 3.0))
    Monster.AddHp(builder, 300)
    Monster.AddName(builder, name)
    Monster.AddInventory(builder, inv)
    Monster.AddColor(builder,
                                        Color.Color().Red)
    Monster.AddWeapons(builder, weapons)
    Monster.AddEquippedType(
        builder, Equipment.Equipment().Weapon)
    Monster.AddEquipped(builder, axe)
    Monster.AddPath(builder, path)
    orc = Monster.End(builder)

    # Call `Finish()` to instruct the builder that this monster is complete.
    builder.Finish(orc)
    # This must be called after `Finish()`.
    buf = builder.Output() # Of type `bytearray`.

    # Get an accessor to the root object inside the buffer.
    monster = Monster.Monster.GetRootAs(buf, 0)
    hp = monster.Hp()
    mana = monster.Mana()
    name = monster.Name()
    pos = monster.Pos()
    # x = pos.X()
    # y = pos.Y()
    # z = pos.Z()

    inv_len = monster.InventoryLength()
    third_item = monster.Inventory(2)

    # weapons_length = monster.WeaponsLength()
    # second_weapon_name = monster.Weapons(1).Name()
    # second_weapon_damage = monster.Weapons(1).Damage()

    union_type = monster.EquippedType()
    # if union_type == Equipment.Equipment().Weapon:
    #     # `monster.Equipped()` returns a `flatbuffers.Table`, which can be used to
    #     # initialize a `Weapon.Weapon()`.
    #     union_weapon = Weapon.Weapon()
    #     union_weapon.Init(monster.Equipped().Bytes, monster.Equipped().Pos)
        
    #     weapon_name = union_weapon.Name()     // 'Axe'
    #     weapon_damage = union_weapon.Damage() // 5

def main():
    # Assuming you have the serialized data from the C++ program
    serialized_data = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x0a\x00\x00\x00John Doe\x1e\x00\x00\x00'
    
    # Create a flatbuffer object from the serialized data
    buf = bytearray(serialized_data)
    person = Person.Person.GetRootAsPerson(buf, 0)

    # Access the fields
    print(f"ID: {person.Id()}")
    # print(f"Name: {person.Name().decode('utf-8')}")
    print(f"Name: {person.Name()}")
    print(f"Age: {person.Age()}")

    testMonster()

if __name__ == "__main__":
    main()
