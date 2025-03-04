document.getElementById('transaction-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const accountID = document.getElementById('accountID').value;
  const amount = document.getElementById('amount').value;
  const transactionDate = document.getElementById('transactionDate').value;

  const payload = { accountID, amount, transactionDate };
  console.log('sending transaction', payload);

  try {
    const response = await fetch('http://localhost:5000/transactions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const result = await response.json();
    alert(result.message);
  } catch (error) {
    alert('Failed to send transaction');
  } finally {
    loadTransactions();
  }
});

// Fetch and display transactions
async function loadTransactions() {
  const response = await fetch('http://localhost:5000/transactions');
  const transactions = await response.json();
  const transactionsList = document.getElementById('transactions');
 transactionsList.innerHTML = transactions.map(transaction => {
    const date = new Date(transaction.transactionDate);
    return `<li>${date.toDateString()} - $${transaction.amount} - Account ID: ${transaction.accountID}</li>`;
  }).join('');
}

loadTransactions();