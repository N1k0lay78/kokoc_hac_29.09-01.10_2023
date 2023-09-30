const ctx = document.getElementById('myChart');

new Chart(ctx, {
    type: 'line',
    data: {
        labels: [1, 2, 3, 4, 5, 6, 7],
        datasets: [{
            label: 'Ваш результат',
            data: [7, 9, 6, 9, 6, 7, 9, 7],
            borderWidth: 2,
            cubicInterpolationMode: 'monotone',
            borderColor: '#1A265A',
            backgroundColor: '#1A265A',
            pointStyle: false,
            tension: 0.4
        }, {
            label: 'Средний в компании',
            data: [8, 8, 8, 8, 8, 8, 8],
            borderWidth: 2,
            cubicInterpolationMode: 'monotone',
            borderColor: '#12b357',
            backgroundColor: '#12b357',
            pointStyle: false,
            tension: 0.4
        }, {
            label: 'Ваш средний результат',
            data: [7, 7, 7, 7, 7, 7, 7],
            borderWidth: 2,
            cubicInterpolationMode: 'monotone',
            borderColor: '#b34709',
            backgroundColor: '#b34709',
            pointStyle: false,
            tension: 0.4
        }]
    },
    options: {
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'bottom',
            },
            title: {
                display: true,
                text: 'Анжумания',
                font: {
                    size: 18,
                },
                padding: {
                    bottom: 5
                }
            },
            subtitle: {
                display: true,
                text: 'Chart Subtitle',
                font: {
                    size: 16,
                },
                padding: {
                    bottom: 20
                }
            }
        },
    },
});