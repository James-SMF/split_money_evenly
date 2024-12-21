// static/script.js

let events = [];
console.log("Events:", events);

// Helper functions
function closeModal() {
    console.log("Closing modal");
    document.getElementById("modal").classList.add("hidden");
    clearModal();
}

function openModal() {
    console.log("Opening modal");
    document.getElementById("modal").classList.remove("hidden");
}

function clearModal() {
    document.getElementById("event-name").value = "";
    document.getElementById("participants").innerHTML = `
        <input type="text" class="participant">
        <button id="add-participant">+</button>
    `;
    document.getElementById("details").innerHTML = "";
}

function calculateFinalBalances() {
    const balances = {}; // { person: net_balance }

    events.forEach(event => {
        const participants = event.participants;
        const transactions = event.transactions;
        const perPersonShare = transactions.reduce((total, t) => total + t.amount, 0) / participants.length;

        participants.forEach(person => {
            if (!balances[person]) balances[person] = 0;
            balances[person] -= perPersonShare;
        });

        transactions.forEach(t => {
            if (t.type === "pay") {
                if (!balances[t.from]) balances[t.from] = 0;
                balances[t.from] += t.amount;
            } else if (t.type === "transfer") {
                if (!balances[t.from]) balances[t.from] = 0;
                if (!balances[t.to]) balances[t.to] = 0;
                balances[t.from] -= t.amount;
                balances[t.to] += t.amount;
            }
        });
    });

    // Output final balances
    const results = [];
    for (const [person, balance] of Object.entries(balances)) {
        if (balance > 0) {
            results.push(`${person} should receive ${balance.toFixed(2)}`);
        } else if (balance < 0) {
            results.push(`${person} should pay ${Math.abs(balance).toFixed(2)}`);
        }
    }

    alert(results.join("\n"));
}

// Event handlers
document.getElementById("new-event-btn").addEventListener("click", openModal);

document.getElementById("cancel").addEventListener("click", closeModal);

document.getElementById("add-participant").addEventListener("click", () => {
    if (event.target.id === "add-participant") {
        const participantsDiv = document.getElementById("participants");

        // 创建新的输入框
        const newInput = document.createElement("input");
        newInput.type = "text";
        newInput.className = "participant";

        // 将输入框插入到加号按钮之前
        participantsDiv.insertBefore(newInput, participantsDiv.lastElementChild);
    }
});

document.getElementById("add-detail").addEventListener("click", () => {
    const detailsDiv = document.getElementById("details");
    const detailRow = document.createElement("div");
    detailRow.className = "detail-row";
    detailRow.innerHTML = `
        <select>
            <option value="transfer">Transfer</option>
            <option value="pay">Pay</option>
        </select>
        <input type="text" class="person-from" placeholder="Person From">
        <span class="arrow">-></span>
        <input type="text" class="person-to" placeholder="Person To">
        <input type="number" class="amount" placeholder="Amount">
    `;
    detailsDiv.appendChild(detailRow);
});

document.getElementById("confirm").addEventListener("click", () => {
    const eventName = document.getElementById("event-name").value;
    const participantInputs = document.querySelectorAll(".participant");
    const participants = Array.from(participantInputs).map(input => input.value).filter(v => v.trim() !== "");

    const transactionRows = document.querySelectorAll("#details .detail-row");
    const transactions = Array.from(transactionRows).map(row => {
        const type = row.querySelector("select").value;
        const from = row.querySelector(".person-from").value;
        const to = row.querySelector(".person-to").value;
        const amount = parseFloat(row.querySelector(".amount").value);
        return { type, from, to, amount };
    });

    events.push({ name: eventName, participants, transactions });

    const eventContainer = document.getElementById("event-container");
    const eventDiv = document.createElement("div");
    eventDiv.className = "event";
    eventDiv.innerHTML = `
        <h3>${eventName}</h3>
        <p>Participants: ${participants.join(", ")}</p>
        <button class="modify">修改</button>
        <button class="delete">删除</button>
    `;

    eventDiv.querySelector(".delete").addEventListener("click", () => {
        const index = events.findIndex(e => e.name === eventName);
        events.splice(index, 1);
        eventDiv.remove();
    });

    eventContainer.appendChild(eventDiv);
    closeModal();
});

// Final calculation
const calculateButton = document.createElement("button");
calculateButton.textContent = "计算结果";
calculateButton.addEventListener("click", calculateFinalBalances);
document.querySelector(".container").appendChild(calculateButton);

