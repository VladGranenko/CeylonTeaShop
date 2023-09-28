            /* PRODUCT BLOCK  */
const productSelect = document.getElementById('productSelect');
const priceProductDisplay = document.getElementById('priceProductDisplay');

productSelect.addEventListener('change', function () {
    const selectedProduct = this.value;
    fetch(`/get_price?product_name=${selectedProduct}`).then(response => response.json()).then(data => {
        if (data.price) {
            priceProductDisplay.textContent = `${data.price}`;
        } else {
            priceProductDisplay.textContent = ' ';
        }
        if (data.definition) {
            infoProductLine.innerHTML = data.definition;
        } else {
            infoProductLine.textContent = ' ';
        }
    }).catch(error => {
        console.error('Error:', error);
    });
});

            /* SERVICE BLOCK  */
const serviceSelect = document.getElementById('serviceSelect');
const priceServiceDisplay = document.getElementById('priceServiceDisplay');

serviceSelect.addEventListener('change', function () {
    const selectedService = this.value;
    fetch(`/get_price?service_name=${selectedService}`).then(response => response.json()).then(data => {
        if (data.price) {
            priceServiceDisplay.textContent = `${data.price}`;
        } else {
            priceServiceDisplay.textContent = ' ';
        }
        if (data.definition) {
            infoServiceLine.innerHTML = data.definition;
        } else {
            infoServiceLine.textContent = ' ';
        }
    }).catch(error => {
        console.error('Error:', error);
    });
});

            /*  DELETE NODES */
$(document).ready(function() {
    $(".delete-button").click(function() {
        var productId = $(this).data("id");
        console.log(productId);
        $.ajax({
            type: "POST",
            url: "/ceylon-tea-shop/delete/" + productId,
            success: function(response) {
                location.reload();
            },
            error: function() {
                alert("Помилка пiд час видалення.");
            }
        });
    });
});

            /* INFO PRODUCT INVISIBLE */
const infoProductLine = document.querySelector('.info-product-line');
const infoProductBox = document.querySelector('.info-product-box');

infoProductBox.addEventListener('click', function(){
    if(infoProductLine.style.display == 'none' && productSelect.value != '-'){
        infoProductLine.style.display = 'block';
    } else {
        infoProductLine.style.display = 'none';
    }
})

            /* INFO SERVICE INVISIBLE */
const infoServiceLine = document.querySelector('.info-service-line');
const infoServiceBox = document.querySelector('.info-service-box');

infoServiceBox.addEventListener('click', function(){
    if(infoServiceLine.style.display == 'none' && serviceSelect.value != '-'){
        infoServiceLine.style.display = 'block';
    } else {
        infoServiceLine.style.display = 'none';
    }
})

            /* DOWNLOAD INVOICE */
const btnBuy = document.querySelector('.main .btn-buy');
const btnLoadExcel = document.getElementById("load-pdf-file");

const loadInvBlock = document.querySelector('.main .invoices-block');
loadInvBlock.style.display = 'none';
function toggleLoadInvBlock() {
    if (loadInvBlock.style.display === 'none') {
        loadInvBlock.style.display = 'block';
    } else {
        loadInvBlock.style.display = 'none';
    }
}
                /* PRESS BUY BUTTON */
if (btnBuy) {
    btnBuy.addEventListener('click', toggleLoadInvBlock);
}
                /* PRESS LOAD BUTTON */

if (btnLoadExcel) {
    btnLoadExcel.addEventListener('click', toggleLoadInvBlock);
}
