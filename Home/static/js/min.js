
//   profile message notification
    function removeToast(element) {
    
        const toast = element.closest('.custom-toast');
        if (toast) {
            toast.classList.add('slide-out-right'); 
            setTimeout(() => {
                toast.remove(); 
            }, 500);
        }
    }

 document.addEventListener('DOMContentLoaded', function() {

    const toasts = document.querySelectorAll('.custom-toast');
    toasts.forEach(toast => {
        setTimeout(() => {
            if (toast.parentNode) {
                toast.classList.add('slide-out-right');
                setTimeout(() => toast.remove(), 500);
            }
        }, 4000);
    });


    const burgerCard = document.getElementById('burger-offer-card');
    if (burgerCard) {
        setTimeout(() => {
            burgerCard.classList.add('show');
        }, 3000); 
    }

    var itemsToShow = 6; 
        var $grid = $('.grid').isotope({
            itemSelector: '.all',
            layoutMode: 'fitRows'
        });

        function updateVisibility() {
            var visibleItems = 0;
            var filterValue = $('.filters_menu li.active').attr('data-filter');
            
            $grid.find(filterValue === '*' ? '.all' : filterValue).each(function (i) {
                if (i < itemsToShow) {
                    $(this).show();
                    visibleItems++;
                } else {
                    $(this).hide();
                }
            });

            var totalItems = $grid.find(filterValue === '*' ? '.all' : filterValue).length;
            if (visibleItems >= totalItems) {
                $('.btn-box').hide();
            } else {
                $('.btn-box').show();
            }

            $grid.isotope('layout');
        }

     
        $('.btn-box a').on('click', function (e) {
            e.preventDefault();
            itemsToShow += 6;
            updateVisibility();
        });

      
        $('.filters_menu li').on('click', function () {
            $('.filters_menu li').removeClass('active');
            $(this).addClass('active');
            itemsToShow = 6; 
            updateVisibility();
        });

     
        updateVisibility();
});


function hideBurgerOffer() {
    const card = document.getElementById('burger-offer-card');
    if (card) {
        card.style.bottom = "-400px"; 
        setTimeout(() => {
            card.remove(); 
        }, 800);
    }
}
    // end of profile message notification
    
    // password do not match error
  document.getElementById('registerForm').addEventListener('submit', function(event) {
        var password = document.getElementById('password').value;
        var confirmPassword = document.getElementById('confirmPassword').value;
        if (password !== confirmPassword) {
            event.preventDefault();
            document.getElementById('error').textContent = "Passwords do not match";
        }
    });









   
