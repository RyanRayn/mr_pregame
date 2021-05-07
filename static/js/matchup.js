
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
    var home_runs = home.reverse();
    var away_runs = away.reverse();
    var runChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                label: home_team,
                data: home_runs,
                lineTension: 0.3,
                backgroundColor: [
                    '#C1E6FF'
                ],
                borderColor: [
                    '#C1E6FF'
                ],
                borderWidth: 3
                },
                {
                    label: away_team,
                    data: away_runs,
                    reverse: true,
                    lineTension: 0.3,
                    backgroundColor: [
                        '#FF7C1F'
                    ],
                    borderColor: [
                        '#FF7C1F'
                    ],
                    borderWidth: 3
                    }
            ]
        },
        options: {
            parsing: {
                xAxisKey: 'runs',
            },
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                },
                x: {}
            }
        },
    });
