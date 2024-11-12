import json
import datetime


def parse_metamask_persist_root(file_path):
    wallets = []
    contacts = []
    transactions = []
    browser_history = []

    with open(file_path, "r", encoding = "utf-8") as file:
        data = json.load(file)

        if 'engine' in data:
            json_object = json.loads(data['engine'])
            json_browser = json.loads(data['browser'])

            # Extract wallet information
            for accs in json_object['backgroundState']['AccountTrackerController']['accounts']:
                s = json_object['backgroundState']['PreferencesController']['identities'][accs]['importTime'] / 1000.0
                import_time = datetime.datetime.fromtimestamp(s).strftime('%Y-%m-%d %H:%M:%S.%f')
                balance = int(
                    str(json_object['backgroundState']['AccountTrackerController']['accounts'][accs]['balance']), 16)
                wallets.append({
                    'import_time': import_time,
                    'wallet_name': json_object['backgroundState']['PreferencesController']['identities'][accs]['name'],
                    'wallet_address': accs,
                    'balance': balance / (10 ** 18)
                })

            # Extract contacts information
            for contactId in json_object['backgroundState']['AddressBookController']['addressBook']:
                for contact in json_object['backgroundState']['AddressBookController']['addressBook'][contactId]:
                    contacts.append({
                        'contact_name':
                            json_object['backgroundState']['AddressBookController']['addressBook'][contactId][contact][
                                'name'],
                        'wallet_address':
                            json_object['backgroundState']['AddressBookController']['addressBook'][contactId][contact][
                                'address']
                    })

            # Extract transactions information
            for transaction in json_object['backgroundState']['TransactionController']['transactions']:
                # print(transaction)
                s = transaction['time'] / 1000.0
                transaction_time = datetime.datetime.fromtimestamp(s).strftime('%Y-%m-%d %H:%M:%S.%f')
                transaction_value = int(str(transaction['txParams']['value']), 16) / (10 ** 18)

                transactions.append({
                    'timestamp': transaction_time,
                    'from': transaction['txParams']['from'],
                    'to': transaction['txParams']['to'],
                    'value': transaction_value,
                    'transaction_hash': transaction.get('hash'),
                    'error': transaction.get('error')
                })

            # Extract browser history information
            for history in json_browser["history"]:
                browser_history.append({
                    'name': history["name"],
                    'url': history["url"]
                })

    # Print the extracted information
    print("Wallets:")
    for wallet in wallets:
        print(wallet)

    print("\nContacts:")
    for contact in contacts:
        print(contact)

    print("\nTransactions:")
    for transaction in transactions:
        print(transaction)

    print("\nBrowser History:")
    for entry in browser_history:
        print(entry)


# Example usage
file_path = r"persist-root.json"
parse_metamask_persist_root(file_path)
