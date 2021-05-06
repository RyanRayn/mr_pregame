
    $(document).ready(function () {
        /* Add 'active' to First Game in For Loop in the Game Carousel */
        $('#game-carousel').find('.carousel-item').first().addClass('active');

        /* Always Make One Accordion Card Stay Open*/
        $('.btn-link').on('click', function() {
            if (!$(this).hasClass('collapsed')) {
                $($('.btn-link').not(this).data('target')).collapse('show')
            }
        });

        /* Click on Picture in Twitter Feed and Expand into Modal */
        $('.pop').on('click', function() {
            $('.media-modal').attr('src', $(this).find('img').attr('src'));
            $('#mediaModal').modal('show');
        });
    });
    
    var ctx = document.getElementById('runChart').getContext('2d');
    var runChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Runs per game',
                data: data,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
