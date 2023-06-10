# Billetera App

**BilleterApp** es un proyecto personal para el registro y control de gastos de dinero a traves de diferentes (e ilimitadas) cuentas, dado que las apps moviles disponibles exigen el uso de la versión paga para poder disfrutar de simples features como por ejemplo "tener más de 3 cuentas". La idea de esta "app" es poder centralizar cómodamente en un solo lugar los gastos o ingresos de dineron de una persona. Está en constante evolución y siempre en búsqueda de implementar features que faciliten su uso.

La principal desventaja es que es un programa para usar en una PC, con lo cual no es portable. Eventualmente haré la versión web que se mantendrá sincronizada con la versión local, pero falta para que eso sea posible.

### Estructura

```
BilleteraAPP
    |__ main.py
    |__ source
        |__ info.py
        |__ users.py
        |__ errors.py
        |__ accounts.py
        |__ analysis.py
        |__ currency.py
        |__ colorizer.py
        |__ operations.py
        |__ sqlpasswd.py
        |__ users_core.py
        |__ account_core.py
        |__ operations_core.py
    |__ data
        |__ userUSR
        |__ passwords.sql
    |__ guicore
	|__ uis
	|__ accounts_gui.py
	|__ calendardialog.py
	|__ categorypiechart.py
	|__ confirmation_dialog.py
	|__ createaccountscreen.py
	|__ createuserscreen.py
	|__ deleteuserscreen.py
	|__ incomeexpensescreen.py
	|__ loginscreen.py
	|__ operationscreen.py
    |__ tests
        |__ tests_accounts_core.py
        |__ tests_accounts_users.py
        |__ tests_operations_core.py
        |__ tests_operations_user.py
        |__ tests_login.py
        |__ tests_users.py
    |__ requirements.txt
    |__ .gitignore
    |__ __pycache__
```
