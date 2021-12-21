"""
Solution to Advent of Code 2021, Day 16.
No docstrings since it seemed redundant.
Possible to simplify parse_operator_packet() and putting the remaining code in read_packet(), but at the cost of
readability.
"""

from operator import mul
import functools
from typing import List


# Multiply list of literal values
def mult(values: List[int]) -> int:
    return functools.reduce(mul, values, 1)


def gt(values: List[int]) -> int:
    if values[0] > values[1]:
        return 1
    else:
        return 0


def lt(values: List[int]) -> int:
    if values[0] < values[1]:
        return 1
    else:
        return 0


def eq(values: List[int]) -> int:
    if values[0] == values[1]:
        return 1
    else:
        return 0


# Hexadecimal to binary.
def hex_to_bin(hex_data: str) -> str:
    total_bin_bit_size = len(hex_data) * 4  # Each hexadecimal corresponds to 4 bits of binary data.
    # Needs to convert hex_input to integer before converting to binary. Removes leading 0b.
    # Fills with starting zeros until the bit size equals that of total_bin_bit_size
    bin_data = bin(int(hex_data, base=16))[2:].zfill(total_bin_bit_size)

    return bin_data


# Binary data to int
def bin_to_int(bin_data: str) -> int:
    return int(bin_data, 2)


# Reads header, returning version number and packet type ID.
def read_header(packet: str) -> (int, int):
    return bin_to_int(packet[0:3]), bin_to_int(packet[3:6])


# Used recursively, mostly. Stores literal values in list 'values'.
def read_packet(packet: str) -> (int, str):
    # Function placed inside parse_packet() to keep list_value_list in correct scope.
    def parse_operator_packet(packet):
        length_type_id, packet = bin_to_int(packet[0]), packet[1:]

        if length_type_id == 0:  # 15 bits after length_type_id represents the subpacket's size in bits
            length_size = 15  # The number of following bits which represent the packet's body's size in number of bits.
            packet_size_bits, packet = bin_to_int(packet[0:length_size]), packet[length_size:]  # Subpacket's size in bits
            subpacket, packet = packet[0:packet_size_bits], packet[packet_size_bits:]

            while (subpacket):  # Until a subpacket isn't returned.
                value, subpacket = read_packet(subpacket)
                values.append(value)

        elif length_type_id == 1:  # 11 bits after length_type_id represents the subpacket's size in subpackets.
            length_size = 11  # Following bits which represent the packet's body's size in number of subpackets.
            packet_size_subpackets, packet = bin_to_int(packet[0:length_size]), packet[length_size:]

            for _ in range(packet_size_subpackets):  # For number of subpackets which make up the packet.
                value, packet = read_packet(packet)
                values.append(value)

        return packet

    (version, type_id), packet = read_header(packet), packet[6:]
    versions.append(version)

    if type_id == 4:
        value, packet = parse_literal_packet(packet)
    else:
        values = []
        packet = parse_operator_packet(packet)  # Saves values in list 'values'
        if type_id == 0:
            value = sum(values)
        elif type_id == 1:
            value = mult(values)
        elif type_id == 2:
            value = min(values)
        elif type_id == 3:
            value = max(values)
        elif type_id == 5:
            value = gt(values)
        elif type_id == 6:
            value = lt(values)
        elif type_id == 7:
            value = eq(values)

    return value, packet


# Parses and reads literal packet. Returns literal value and rest of packet.
def parse_literal_packet(packet: str) -> (int, str):
    bits_per_subpacket = 5
    packet_lit_val_bin = ""  # To store the parsed literal value of the packet in binary form

    subpacket_number = 1
    while(True):  # Parsing and reading each subpacket until finding last one.
        lower_limit = (subpacket_number - 1) * bits_per_subpacket
        upper_limit = subpacket_number * bits_per_subpacket
        subpacket = packet[lower_limit:upper_limit]
        packet_lit_val_bin += subpacket[1:bits_per_subpacket]  # 0th bit indicates if it's the last subpacket or not

        if bin_to_int(subpacket[0]) == 0:  # Indicates that subpacket is last packet's body.
            num_of_subpackets = subpacket_number  # Total number of subpackets
            break
        subpacket_number += 1

    bits_read = num_of_subpackets * bits_per_subpacket  # The total size in bits of the body of the literal packet
    lit_val = bin_to_int(packet_lit_val_bin)

    return lit_val, packet[bits_read:]


# Read the hexadecimal transmission
def read_transmission(hex_data: str) -> (int, int):
    versions.clear()  # In case read_transmission() is to be run more than once.
    packet = hex_to_bin(hex_data)
    value, _ = read_packet(packet)  # Only the resulting value is of use at this level.
    sum_versions = sum(versions)

    return sum_versions, value


if __name__ == '__main__':
    versions = []  # Global variable to collect all the version numbers.
    sum_versions, value = read_transmission("E20D4100AA9C0199CA6A3D9D6352294D47B3AC6A4335FBE3FDD251003873657600B46F8DC600AE80273CCD2D5028B6600AF802B2959524B727D8A8CC3CCEEF3497188C017A005466DAA6FDB3A96D5944C014C006865D5A7255D79926F5E69200A164C1A65E26C867DDE7D7E4794FE72F3100C0159A42952A7008A6A5C189BCD456442E4A0A46008580273ADB3AD1224E600ACD37E802200084C1083F1540010E8D105A371802D3B845A0090E4BD59DE0E52FFC659A5EBE99AC2B7004A3ECC7E58814492C4E2918023379DA96006EC0008545B84B1B00010F8E915E1E20087D3D0E577B1C9A4C93DD233E2ECF65265D800031D97C8ACCCDDE74A64BD4CC284E401444B05F802B3711695C65BCC010A004067D2E7C4208A803F23B139B9470D7333B71240050A20042236C6A834600C4568F5048801098B90B626B00155271573008A4C7A71662848821001093CB4A009C77874200FCE6E7391049EB509FE3E910421924D3006C40198BB11E2A8803B1AE2A4431007A15C6E8F26009E002A725A5292D294FED5500C7170038C00E602A8CC00D60259D008B140201DC00C401B05400E201608804D45003C00393600B94400970020C00F6002127128C0129CDC7B4F46C91A0084E7C6648DC000DC89D341B23B8D95C802D09453A0069263D8219DF680E339003032A6F30F126780002CC333005E8035400042635C578A8200DC198890AA46F394B29C4016A4960C70017D99D7E8AF309CC014FCFDFB0FE0DA490A6F9D490010567A3780549539ED49167BA47338FAAC1F3005255AEC01200043A3E46C84E200CC4E895114C011C0054A522592912C9C8FDE10005D8164026C70066C200C4618BD074401E8C90E23ACDFE5642700A6672D73F285644B237E8CCCCB77738A0801A3CFED364B823334C46303496C940")
    print(f"Sum of versions is {sum_versions} and value is {value}")
