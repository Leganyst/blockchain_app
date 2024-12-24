import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
    QHBoxLayout, QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox
)
from eth_account import Account
from web3 import Web3
from config import ADDRESS, PRIVATE_KEY, NETWORK_URL, SMART_CONTRACT_ADDRESS, SMART_CONTRACT_ABI
from erc20_config import ERC20_ADDRESS, ERC20_ABI



from web3 import Web3
from eth_account import Account


class InsuranceData:
    def __init__(self, contract_address, abi, private_key, network_url, token_address, token_abi):
        self.web3: Web3 = Web3(Web3.HTTPProvider(network_url))
        if not self.web3.is_connected():
            raise Exception("Не удалось подключиться к сети Ethereum")
        
        # Связь с токенами
        self.token = self.web3.eth.contract(address=token_address, abi=token_abi)
        
        # Связь с контрактом
        self.contract_address = contract_address
        self.contract = self.web3.eth.contract(address=contract_address, abi=abi)
        
        # Устанавливаем аккаунт
        self.private_key = private_key
        self.account = Account.from_key(private_key)

    def get_balance(self):
        try:
            balance = self.token.functions.balanceOf(self.account.address).call()
            return balance
        except Exception as e:
            print(f"Failed to get balance: {e}")
            return None

    def create_policy(self, policy_holder, premium, coverage, duration_type):
        try:
            # Преобразовываем адрес пользователя в checksum-формат
            policy_holder_checksum = self.web3.to_checksum_address(policy_holder)

            # Получаем текущий nonce
            nonce = self.web3.eth.get_transaction_count(self.account.address, 'pending')

            # Шаг 1: Авторизация токенов (approve)
            approval_tx = self.token.functions.approve(
                self.contract_address,
                int(premium)
            ).build_transaction({
                "from": self.account.address,
                "nonce": nonce,
                "gas": 5000000,
                "gasPrice": self.get_gas_price()
            })

            signed_approval_tx = self.web3.eth.account.sign_transaction(approval_tx, self.private_key)
            approval_tx_hash = self.web3.eth.send_raw_transaction(signed_approval_tx.raw_transaction)
            self.web3.eth.wait_for_transaction_receipt(approval_tx_hash)
            print(f"Approval transaction hash: {approval_tx_hash.hex()}")

            # Проверяем, что токены успешно авторизованы
            nonce += 1
            allowance = self.token.functions.allowance(self.account.address, self.contract_address).call()
            if allowance < premium:
                print("Allowance is less than the required premium.")
                return None

            # Проверяем баланс
            balance = self.get_balance()
            if balance is None or balance < premium:
                print("Insufficient balance.")
                return None

            gas_limit = self.contract.functions.createPolicy(
                policy_holder_checksum, premium, coverage, duration_type
            ).estimate_gas({
                "from": self.web3.to_checksum_address(self.account.address)
            })
            print(f"Estimated Gas: {gas_limit}")
            
            # Шаг 2: Создание полиса
            transaction = self.contract.functions.createPolicy(
                policy_holder_checksum,
                premium,
                coverage,
                duration_type  # Используем стандартизированный тип продолжительности
            ).build_transaction({
                "from": self.account.address,
                "nonce": nonce,
                "gas": 5000000,
                "gasPrice": self.get_gas_price()
            })

            signed_tx = self.web3.eth.account.sign_transaction(transaction, self.private_key)
            tx_hash = self.web3.eth.send_raw_transaction(signed_tx.raw_transaction)
            receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
            print(f"Transaction Receipt: {receipt}")

            # Проверяем события Debug
            logs = self.contract.events.Debug().process_receipt(receipt)
            for log in logs:
                print(f"Debug Message: {log['args']['message']}")

            return tx_hash.hex()

        except Exception as e:
            print(f"Failed to create policy: {e}")
            return None

    def get_user_policies(self, user):
        try:
            user_checksum = self.web3.to_checksum_address(user)

            # Получаем список policyId
            policy_ids = self.contract.functions.getUserPolicies(user_checksum).call()

            # Список полисов
            user_policies = []
            for policy_id in policy_ids:
                try:
                    policy_info = self.contract.functions.getUserPolicyInfo(user_checksum, policy_id).call()
                    policy_data = {
                        "id": policy_info[0],
                        "policyHolder": policy_info[1],
                        "premium": policy_info[2],
                        "coverageAmount": policy_info[3],
                        "startDate": policy_info[4],
                        "endDate": policy_info[5],
                        "isActive": policy_info[6],
                        "isClaimed": policy_info[7],
                    }
                    user_policies.append(policy_data)
                except Exception as e:
                    print(f"Failed to fetch policy info for ID {policy_id}: {e}")

            return user_policies
        except Exception as e:
            print(f"Failed to get user policies: {e}")
            return []

    def claim_policy(self, policy_id):
        try:
            nonce = self.web3.eth.get_transaction_count(self.account.address, 'pending')
            gas_price = self.get_gas_price()

            # Оценка газа
            gas_limit = self.contract.functions.claim(policy_id).estimate_gas({
                "from": self.account.address
            })

            # Создание транзакции
            transaction = self.contract.functions.claim(policy_id).build_transaction({
                "from": self.account.address,
                "nonce": nonce,
                "gas": gas_limit,
                "gasPrice": gas_price,
            })

            # Подписываем и отправляем транзакцию
            signed_tx = self.web3.eth.account.sign_transaction(transaction, self.private_key)
            tx_hash = self.web3.eth.send_raw_transaction(signed_tx.raw_transaction)
            print(f"Transaction sent! Hash: {tx_hash.hex()}")

            # Ожидание подтверждения
            receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
            print(f"Transaction confirmed! Receipt: {receipt}")

            return tx_hash.hex()

        except Exception as e:
            print(f"Failed to claim policy: {e}")
            return None

    def get_gas_price(self):
        try:
            return self.web3.eth.gas_price
        except Exception as e:
            print(f"Failed to fetch gas price: {e}")
            return self.web3.to_wei("10", "gwei")


from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QVBoxLayout, QLineEdit, QPushButton, QLabel, 
    QTableWidget, QTableWidgetItem, QMessageBox, QWidget
)
from datetime import datetime
import sys

# Вставить сюда InsuranceData и настройки для работы с блокчейном


class InsuranceGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insurance GUI")
        self.setGeometry(100, 100, 800, 600)
        
        self.data = InsuranceData(SMART_CONTRACT_ADDRESS, SMART_CONTRACT_ABI, PRIVATE_KEY,
                                  NETWORK_URL, ERC20_ADDRESS, ERC20_ABI)
        
        self.main_layout = QVBoxLayout()
        self.init_ui()
        
        container = QWidget()
        container.setLayout(self.main_layout)
        self.setCentralWidget(container)
        
    def init_ui(self):
        self.policy_holder_input = QLineEdit()
        self.policy_holder_input.setPlaceholderText("Policy Holder Address")
        
        self.premium_input = QLineEdit()
        self.premium_input.setPlaceholderText("Premium Amount")
        
        self.coverage_input = QLineEdit()
        self.coverage_input.setPlaceholderText("Coverage Amount")
        
        self.duration_input = QLineEdit()
        self.duration_input.setPlaceholderText("Duration in months")
        
        create_button = QPushButton("Create Policy")
        create_button.clicked.connect(self.create_policy)
        
        self.main_layout.addWidget(QLabel("Create New Policy"))
        self.main_layout.addWidget(self.policy_holder_input)
        self.main_layout.addWidget(self.premium_input)
        self.main_layout.addWidget(self.coverage_input)
        self.main_layout.addWidget(self.duration_input)
        self.main_layout.addWidget(create_button)
        
        self.policies_table = QTableWidget()
        self.policies_table.setColumnCount(7)
        self.policies_table.setHorizontalHeaderLabels([
            "ID", "Policy Holder", "Premium", "Coverage", 
            "Start Date", "End Date", "Is Active"
        ])
        self.main_layout.addWidget(QLabel("Your Policies"))
        self.main_layout.addWidget(self.policies_table)

        refresh_button = QPushButton("Refresh Policies")
        refresh_button.clicked.connect(self.refresh_policies)
        self.main_layout.addWidget(refresh_button)
        
        claim_button = QPushButton("Claim Policy")
        claim_button.clicked.connect(self.claim_policy)
        self.main_layout.addWidget(claim_button)
    
    def format_time(self, timestamp):
        """
        Преобразует Unix timestamp в строку формата 'DD.MM.YYYY HH:MM'.
        """
        try:
            dt = datetime.utcfromtimestamp(timestamp)
            return dt.strftime('%d.%m.%Y %H:%M')
        except Exception as e:
            print(f"Failed to format time: {e}")
            return "Invalid time"
    
    def create_policy(self):
        policy_holder = self.policy_holder_input.text()
        
        try:
            premium = int(self.premium_input.text())
            coverage = int(self.coverage_input.text())
            duration = int(self.duration_input.text())
        except ValueError:
            QMessageBox.warning(self, "Error", "Premium, Coverage, and Duration must be valid numbers.")
            return

        if not all([policy_holder, premium, coverage, duration]):
            QMessageBox.warning(self, "All fields are required")
            return
    
        try:
            tx_hash = self.data.create_policy(policy_holder, premium, coverage, duration)
            QMessageBox.information(self, "Policy Created", f"Transaction Hash: {tx_hash}")
            self.refresh_policies()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to create policy: {e}")

    def refresh_policies(self):
        user_address = self.policy_holder_input.text()
        if not user_address:
            QMessageBox.warning(self, "Error", "Policy Holder Address is required")
            return
            
        try:
            policies = self.data.get_user_policies(user_address)
            self.policies_table.setRowCount(len(policies))
        
            for row_position, policy in enumerate(policies):
                start_date = self.format_time(policy["startDate"])
                end_date = self.format_time(policy["endDate"])
                self.policies_table.setItem(row_position, 0, QTableWidgetItem(str(policy["id"])))
                self.policies_table.setItem(row_position, 1, QTableWidgetItem(policy["policyHolder"]))
                self.policies_table.setItem(row_position, 2, QTableWidgetItem(str(policy["premium"])))
                self.policies_table.setItem(row_position, 3, QTableWidgetItem(str(policy["coverageAmount"])))
                self.policies_table.setItem(row_position, 4, QTableWidgetItem(start_date))
                self.policies_table.setItem(row_position, 5, QTableWidgetItem(end_date))
                self.policies_table.setItem(row_position, 6, QTableWidgetItem("Yes" if policy["isActive"] else "No"))
        except Exception as e:
            QMessageBox.warning(self, "Warning", f"Failed to refresh policies: {e}")     
    
    def claim_policy(self):
        current_row = self.policies_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Error", "Select a policy to claim")
            return

        policy_id = int(self.policies_table.item(current_row, 0).text())
        try:
            tx_hash = self.data.claim_policy(policy_id)
            QMessageBox.information(self, "Success", f"Claim submitted. Transaction Hash: {tx_hash}")
            self.refresh_policies()
        except Exception as e:
            QMessageBox.warning(self, "Warning", f"Failed to claim policy: {e}")
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = InsuranceGUI()
    main_window.show()
    sys.exit(app.exec_())
