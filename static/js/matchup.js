
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

        /* Add green class to higher values in stat-chart */
        $('.higher').each(function() {
            var $tds = $(this).find('td');
            var values = $tds.map(function() {
              return parseFloat($(this).text().trim().replace(',', '.'));
            }).get();
            $tds.eq(values.reduce((iMax, x, i, arr) => x > arr[iMax] ? i : iMax, 0)).removeClass('white opacity-90').addClass('green');
        });

        /* Add green class to lower values in stat-chart */
        $('.lower').each(function() {
            var $tds = $(this).find('td');
            var values = $tds.map(function() {
              return parseFloat($(this).text().trim().replace(',', '.'));
            }).get();
            $tds.eq(values.reduce((iMax, x, i, arr) => x > arr[iMax] ? i : iMax, 0)).removeClass('green').addClass('white opacity-90');
        });
    });
    
    /* Run Trend Chart */
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
            responsive: true,
            maintainAspectRation: true,
            plugins: {
                legend: {
                    labels: {
                        color: 'white',
                        font: {
                            size: 15,
                            family: 'Oswald, sans-serif'
                        }
                    }
                },
                tooltip: {
                    enabled: false,
                },
            },
            scales: {
                y: {
                    title: {
                        display: true,
                        text: 'Runs',
                        color: 'white',
                    },
                    ticks: {
                        color: 'white',
                    },
                    grid:{
                        display: false,
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Games',
                        color: 'white',
                    },
                    ticks: {
                        color: 'white',
                    },
                    grid: {
                        display: false,
                    }
                },
            }
        },
    });
