#!/usr/bin/env python3

from src.proto import ipfs_pb2
import os
import base64
import json
import sys
from google.protobuf.json_format import MessageToDict

result = []
block_file_list = []
cid_path_map= {}

"""
When ipfs is initialized, there are files that are created by default.
We created a blacklist variable to remove unnecessary files from evidence collection.
"""
black_list = [
    "CIQA4T3TD3BP3C2M3GXCGRCRTCCHV7XSGAZPZJOAOHLPOI6IQR3H6YQ",
    "CIQBEM7N2AM5YRAMJY7WDI6TJ4MGYIWVBA7POWSBPYKENY5IKK2I75Y",
    "CIQCXBHBZAHEHBHU6P7PEA72E7UZQRJALHH7OH2FCWSWMTU7DMWVBEA",
    "CIQMDQRK7B5DSZKBYOX4353TGN5J3JXS5VS6YNSAEJBOXBG26R76HBY",
    "CIQBZNLCBI3U2I5F7O636DRBO552SCMSK2X2WYVCQ6BMYJN4MJTRI2Q",
    "CIQJFGRQHQ45VCQLM7AJNF2GF5UHUAGGHC6LLAH6VYDEKLQMD4QLILY",
    "CIQB4655YD5GLBB7WWEUAHCO6QONU5ICBONAA5JEPBIOEIVZ5RXTIYY",
    "CIQPHMHGQLLZXC32FQQW2YVM4KGFORVFJAQYY55VK3WJGLZ2MS4RJNQ",
    "CIQD44K6LTXM6PHWK2RHB3G2VCYFPMVBTALE572GSMETJGBJTELFKEI",
    "CIQHQFRJK4MU2CVNFR3QG6KZB3FZG6OG7EBI4SUNB5K4S4T5UVECMJA",
    "CIQGFYPT5OBMRC7ZMUFC2R3ZQPKOGBMHJEDDFEVS5ALYBKIZCXPTN6Y",
    "CIQBT4N7PS5IZ5IG2ZOUGKFK27IE33WKGJNDW2TY3LSBNQ34R6OVOOQ",
    "CIQL4QZR6XGWMPEV5Q2FCTDFD7MF3G5OOC5CMEDUHNA5VXYZVDLFQDA",
    "CIQBED3K6YA5I3QQWLJOCHWXDRK5EXZQILBCKAPEDUJENZ5B5HJ5R3A",
    "CIQDRD2UT66U4EATJW53PSVWMFFPGNAN42PVWMDLHJD6FA5EVNNZROI",
    "CIQCODPXR5G237BYM7E5JF4A624CLH2TQDLC4QI6HEZK7FUWZQESTPI",
    "CIQHFTCY7XL57YWLVDQ6UAXUOND3ADYQYJKYXA6G7A5IMD7SMO22U2A",
    "CIQFKVEG2CPWTPRG5KNRUAWMOABRSTYUFHFK3QF6KN3M67G5E3ILUCY",
    "CIQAPZYJAKUKALYI4YTB5PUMEN5BZYZHUQZWGFL4Q3HZUV26SYX2V3Q",
    "CIQPEOA2TS3RMLOBOF55ZOEZE3TNBQG3HCNFOYC3BATAIJBOIE5FVNY",
    "CIQFTFEEHEDF6KLBT32BFAGLXEZL4UWFNWM4LFTLMXQBCERZ6CMLX3Y",
    "CIQGAS6MQJCEC37C2IIH5ZFYJCSTT7TCKJP3F7SLGNVSDVZSMACCXVA",
]

def arg_option():
    if len(sys.argv) > 1:
        path = sys.argv[1]
        if os.path.isdir(path):
            return path
        else:
            print("[!] Please enter the correct path")
            exit()
    else:
        print("[!] Please provide the path as an argument.\nex) python3 reassemble_chunks.py [IPFS block Path]")
        exit()


def cidToPath(cid_b64encode, dir_path):
    cid = base64.b64decode(cid_b64encode)
    cid = cid[2:] if cid[0:2] == b"\x01\x55" else cid

    cid_b32encode = base64.b32encode(cid)
    cid_filename = cid_b32encode.decode().replace("=", "")
    block_folder = cid_filename[-3:-1]
    block_path = os.path.join(dir_path, block_folder, cid_filename + ".data")
    return block_path


def extractList(block, dir_path):
    """
    List is like
    {
        "data": ["blob", "list", "blob"],
        "links": [
            {"hash": "XXX", "size": 15123 },
            {"hash": "XXX", "size": 15123 },
            {"hash": "XXX", "size": 15123 }
            // List can't have names
        ]
    }
    """
    list_data = b""
    for links in block["decoded"]["Links"]:
        cid_b64encode = links["Hash"]
        block_path = cidToPath(cid_b64encode, dir_path)
        blob_data = b""
        for search_block in result:
            if search_block["path"] == block_path:
                if search_block["raw"] == True:
                    blob_data = search_block["raw_data"]
                elif bool(search_block["decoded"]) == False:
                    continue
                elif search_block["decoded"]["Data"]["Type"] == "File":
                    if "Links" in search_block["decoded"].keys():
                        blob_data = extractList(search_block, dir_path)
                    else:
                        blob_data = extractblob(search_block)
                break
        list_data += blob_data
    return list_data


def extractblob(block):
    """
    Blob is like
    {
        "data": "some data here"
    }
    """
    if int(block["decoded"]["Data"]["filesize"]) == 0:
        return None
    else:
        content = block["decoded"]["Data"]["Data"]
        return base64.b64decode(content)


def extractTree(block, dir_path, output_path):
    """
    Tree is like
    {
        "data": ["blob", "list", "blob"],
        "links": [
            {"hash": "XXX", "name: "less", "size": 15123 },
            {"hash": "XXX", "name: "less", "size": 15123 },
            {"hash": "XXX", "name: "less", "size": 15123 }
            // Tree can have names
        ]
    }
    """
    folder_name = os.path.splitext(os.path.basename(block["path"]))[0]
    os.makedirs(os.path.join(output_path, folder_name), exist_ok=True)
    if "Links" in block["decoded"]:
        for file in block["decoded"]["Links"]:
            cid_b64encode = file["Hash"]
            filename = file["Name"]
            block_path = cidToPath(cid_b64encode, dir_path)

            # Add to file_mapping.json
            cid = os.path.basename(block_path)
            cid_path_map[cid] = filename

            # Reassemble blocks
            blob_data = b""
            for search_block in result:
                if search_block["path"] == block_path:
                    if search_block["raw"] == True:
                        blob_data = search_block["raw_data"]
                    elif bool(search_block["decoded"]) == False:
                        continue
                    elif search_block["decoded"]["Data"]["Type"] == "Directory":
                        extractTree(search_block, dir_path, output_path)
                    elif (
                        search_block["decoded"]["Data"]["Type"] == "File"
                        and "Links" in search_block["decoded"].keys()
                    ):
                        blob_data = extractList(search_block, dir_path)
                    else:
                        blob_data = extractblob(search_block)
                    break

            if blob_data is not None:
                with open(os.path.join(output_path, folder_name, filename), "wb") as f:
                    f.write(blob_data)


def reassemble_chunks(dir_path, output_path):
    output_path = os.path.join(output_path, "reassemble")
    os.makedirs(output_path, exist_ok=True)
    
    for (root, directories, files) in os.walk(dir_path):
        for file in files:
            file_path = os.path.join(root, file)
            path, ext = os.path.splitext(file_path)
            if ext == ".data":
                if any(bl in file_path for bl in black_list):
                    pass
                else:
                    block_file_list.append(file_path)

    for block_file in block_file_list:
        block_data = open(block_file, "rb").read()
        IPFS = ipfs_pb2.PBNode()
        try:
            # Handle IPFS protobuf block
            IPFS.ParseFromString(block_data)
            block_result = {
                "path": block_file,
                "decoded": [],
                "raw": False,
                "processed": False,
            }
            block_result["decoded"] = MessageToDict(IPFS)
        except:
            block_result = {"path": block_file, "raw_data": block_data, "raw": True}
        finally:
            result.append(block_result)

    # Collect tree first. We use DFS strategy for preventing duplication
    for idx, block in enumerate(result):
        if block["raw"] == True:
            continue
        elif bool(block["decoded"]) == False:
            continue
        elif (
            block["decoded"]["Data"]["Type"] == "Directory"
            and block["processed"] != True
        ):
            extractTree(block, dir_path, output_path)
            result[idx]["processed"] = True

    # Collect list second. We use DFS strategy for preventing duplication
    for idx, block in enumerate(result):
        if block["raw"] == True:
            continue
        elif bool(block["decoded"]) == False:
            continue
        elif block["decoded"]["Data"]["Type"] == "File" and block["processed"] != True:
            if "Links" in block["decoded"].keys():
                file_data = extractList(block, dir_path)
                filename = os.path.splitext(os.path.basename(block["path"]))[0]
                with open(os.path.join(output_path, filename), "wb") as f:
                    f.write(file_data)
                result[idx]["processed"] = True

    # Collect blob third. We use DFS strategy for preventing duplication
    for idx, block in enumerate(result):
        if block["raw"] == True:
            continue
        elif bool(block["decoded"]) == False:
            continue
        elif block["decoded"]["Data"]["Type"] == "File" and block["processed"] != True:
            if "Links" not in block["decoded"].keys():
                file_data = extractblob(block)
                filename = os.path.splitext(os.path.basename(block["path"]))[0]
                with open(os.path.join(output_path, filename), "wb") as f:
                    f.write(file_data)
                result[idx]["processed"] = True

        elif block["decoded"]["Data"]["Type"] not in ("File", "Directory"):
            print(f'[DEBUG] Unknown data type: {block["decoded"]["Data"]["Type"]}')

    # Save file_mapping.json
    j = json.dumps(cid_path_map, indent=4)
    with open(os.path.join(output_path, "file_mapping.json"), "w") as out:
        print(j, file=out)
