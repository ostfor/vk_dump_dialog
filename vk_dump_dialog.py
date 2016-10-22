import argparse
import json
import math
import time
import vk


def get_dialogs(user_id, batch_width=200, config_path="config.json"):
    with open(config_path) as f:
        cfg = json.load(f)
    sess = vk.Session(access_token=cfg["acess_token"])
    api = vk.API(sess)
    data = api.messages.getHistory(user_id=user_id, count=1)
    count = int(data[0])
    messages = []
    for i in range(int(math.ceil(count / batch_width))):
        messages += api.messages.getHistory(user_id=user_id, count=batch_width,
                                            offset=i * batch_width)[1:]
    if count != len(messages):
        print ("Warning: messages count "
               "is not expected {} != {}".format(count, len(messages)))
    return messages


def parse_data_and_print(messages):
    for msg in messages[::-1]:
        print msg['out'], time.asctime(time.gmtime(msg['date'])), msg['body']

def process(user_id, res_file, batch_width=200, config_path="config.json"):
    messages = get_dialogs(user_id, batch_width, config_path)
    with open(res_file, 'w') as f:
        json.dump(messages, f)
    parse_data_and_print(messages)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--user-id", "-u", help="vk user id")
    parser.add_argument("--result-file", "-r",
                        help="path to file to save messages")
    parser.add_argument("--batch-width", "-b", help="width of batch", type=int,
                        default=200)
    parser.add_argument("--config-path", "-c", help="configuration file path",
                        default="config.json")
    args = parser.parse_args()
    process(args.user_id, args.result_file, args.batch_width,
                args.config_path)


if __name__ == '__main__':
    main()
