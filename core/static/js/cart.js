(function () {
    const storageKey = 'elCamaronCrudoCart';

    function getCart() {
        try { return JSON.parse(localStorage.getItem(storageKey)) || []; }
        catch { return []; }
    }

    function saveCart(cart) {
        localStorage.setItem(storageKey, JSON.stringify(cart));
        updateBadge();
    }

    function money(value) {
        return `$${Number(value).toFixed(2)}`;
    }

    function updateBadge() {
        const quantity = getCart().reduce((total, item) => total + item.cantidad, 0);
        document.querySelectorAll('[data-cart-count]').forEach((badge) => { badge.textContent = quantity; });
    }

    function addProduct(button) {
        const product = {
            id: button.dataset.id,
            nombre: button.dataset.nombre,
            precio: Number(button.dataset.precio),
            imagen: button.dataset.imagen,
        };
        const cart = getCart();
        const existing = cart.find((item) => item.id === product.id);
        if (existing) existing.cantidad += 1;
        else cart.push({ ...product, cantidad: 1 });
        saveCart(cart);
        const original = button.textContent;
        button.textContent = '¡Agregado!';
        setTimeout(() => { button.textContent = original; }, 1200);
    }

    function renderCart() {
        const container = document.querySelector('#lista-carrito');
        if (!container) return;
        const cart = getCart();
        const subtotal = cart.reduce((total, item) => total + item.precio * item.cantidad, 0);
        container.innerHTML = cart.length ? cart.map((item) => `
            <article class="card shadow-sm border-0 mb-3"><div class="card-body d-flex align-items-center gap-3">
                <img src="/static/${item.imagen}" alt="${item.nombre}" width="80" height="80" style="object-fit:cover" class="rounded">
                <div class="flex-grow-1"><h2 class="h5 mb-1">${item.nombre}</h2><span class="text-muted">${money(item.precio)} c/u</span></div>
                <div class="input-group" style="width:120px"><button class="btn btn-outline-secondary" data-change="-1" data-id="${item.id}">−</button><span class="form-control text-center">${item.cantidad}</span><button class="btn btn-outline-secondary" data-change="1" data-id="${item.id}">+</button></div>
                <strong>${money(item.precio * item.cantidad)}</strong><button class="btn btn-link text-danger" aria-label="Eliminar ${item.nombre}" data-remove="${item.id}"><i class="bi bi-trash"></i></button>
            </div></article>`).join('') : '<div class="card border-0 shadow-sm"><div class="card-body text-center py-5"><i class="bi bi-cart-x fs-1 text-muted"></i><p class="mt-3 mb-0">Tu carrito está vacío.</p></div></div>';
        document.querySelector('#cart-subtotal').textContent = money(subtotal);
        document.querySelector('#cart-total').textContent = money(subtotal);
        const checkout = document.querySelector('#checkout-button');
        if (checkout) checkout.classList.toggle('disabled', cart.length === 0);
    }

    document.addEventListener('click', (event) => {
        const add = event.target.closest('[data-agregar-carrito]');
        if (add) addProduct(add);
        const change = event.target.closest('[data-change]');
        if (change) {
            const cart = getCart(); const item = cart.find((entry) => entry.id === change.dataset.id);
            if (item) { item.cantidad += Number(change.dataset.change); saveCart(cart.filter((entry) => entry.cantidad > 0)); renderCart(); }
        }
        const remove = event.target.closest('[data-remove]');
        if (remove) { saveCart(getCart().filter((entry) => entry.id !== remove.dataset.remove)); renderCart(); }
    });

    document.querySelector('#payment-form')?.addEventListener('submit', (event) => {
        event.preventDefault();
        const result = document.querySelector('#payment-result');
        result.textContent = 'Pedido de prueba confirmado. No se realizó ningún cobro.';
        result.classList.remove('d-none');
        localStorage.removeItem(storageKey);
        updateBadge();
        event.target.reset();
    });

    updateBadge();
    renderCart();
}());
