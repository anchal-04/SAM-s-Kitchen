document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.counter').forEach(counter => {
        const itemId = counter.getAttribute('data-item-id');
        const countElement = counter.querySelector('.count');
        const decreaseBtn = counter.querySelector('.decrease');
        const increaseBtn = counter.querySelector('.increase');

        decreaseBtn.addEventListener('click', () => updateCart(itemId, 'decrease', countElement, counter));
        increaseBtn.addEventListener('click', () => updateCart(itemId, 'increase', countElement, counter));
    });

    function updateCart(itemId, action, countElement, counter) {
        fetch('/cart/modify', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                item_id: itemId,
                action: action,
            }),
        })
        .then(response => {
            if (response.ok) {
                return response.json(); // Expect a JSON response with updated data
            } else {
                throw new Error('Failed to update cart');
            }
        })
        .then(data => {
            // Update the item's quantity
            let count = parseInt(countElement.textContent);
            if (action === 'increase') count++;
            if (action === 'decrease' && count > 0) count--;
            countElement.textContent = count;

            // Update Sub-Total, Items Count, and Total Price
            document.querySelector('.items').textContent = `${data.total_items} items`;
            document.querySelector('.total-amount').textContent = `$${data.total_price.toFixed(2)}`;
            const itemPrice = parseFloat(counter.querySelector('.amount').textContent.substring(1));
            counter.querySelector('.amount').textContent = `$${(itemPrice * count).toFixed(2)}`;
        })
        .catch(err => alert(err.message));
    }
});