from flask import Flask, jsonify

# 1. Create the Flask App
app = Flask(__name__)

# 2. Mock Finacle Data (In a real system, this would query a database)
MOCKED_FINACLE_DATA = {
    "accounts": {
        "SBA1001": {"status": "ACTIVE", "currency": "INR"},
        "SBA1002": {"status": "DORMANT", "currency": "INR"},
        "CAA2001": {"status": "ACTIVE", "currency": "USD"},
    },
    "userhooks": {
        "urhk_getAcctBalanceAsOnDate": {
            "inputs": ["BANCS.INPARAM.acctId", "BANCS.INPARAM.asOnDate"],
            "outputs": ["BANCS.OUTPARAM.acctBal"],
            "description": "Returns the end-of-day account balance for a given date.",
        },
        "urhk_getAcctStatus": {
            "inputs": ["BANCS.INPARAM.acid"],
            "outputs": ["BANCS.OUTPARAM.acctStatus"],
            "description": "Finds out the status of the given account ID.",
        },
        "urhk_rejithstatus": {
            "inputs": ["BANCS.INPARAM.name"],
            "outputs": ["BANCS.OUTPARAM.fulldata"],
            "description": "This is a test userhook to test the validity of userhook",
        },
    },
}

# 3. Define the "Tools" as API Endpoints


# Tool 1: Validate an Account
@app.route("/tools/validate_account/<account_id>", methods=["GET"])
def validate_account(account_id: str) -> str:
    """
    Checks if an account exists and returns its details.
    Args:
        account_id(str) : account number
    Returns:
        str:
    """
    print(f"MCP Server: Received request to validate account: {account_id}")
    account_details = MOCKED_FINACLE_DATA["accounts"].get(account_id.upper())

    if account_details:
        return jsonify(account_details)
    else:
        return jsonify({"error": "Account not found"}), 404


# Tool 2: Get Userhook Parameters
@app.route("/tools/get_userhook_params/<hook_name>", methods=["GET"])
def get_userhook_params(hook_name):
    """
    Retrieves the input and output parameter details for a specified userhook.

    Args:
        hook_name (str): The name of the userhook whose parameters are to be fetched.

    Returns:
        JSON response containing:
            - inputs (list): List of input parameter names for the userhook.
            - outputs (list): List of output parameter names for the userhook.
            - description (str): Description of the userhook.
        If the userhook is not found, returns a JSON error message with HTTP 404 status.
    """
    print(f"MCP Server: Received request for userhook: {hook_name}")
    hook_details = MOCKED_FINACLE_DATA["userhooks"].get(hook_name)

    if hook_details:
        return jsonify(hook_details)
    else:
        return jsonify({"error": "Userhook not found"}), 404


# 4. Run the Server
if __name__ == "__main__":
    # Runs the server on http://127.0.0.1:5000
    app.run(debug=True, port=5000)
