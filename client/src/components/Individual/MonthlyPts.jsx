import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
import ChartDataLabels from 'chartjs-plugin-datalabels';

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    ChartDataLabels
);

export const MonthlyPoints = (props) => {
    const [points, setPoints] = useState([]);
    
    useEffect(() => {
        if (props.status === 'login') {
            const fetchData = async () => {
                try {
                    const res = await fetch(`/api/individual/${props.id}/monthly_pts`);
                    if (!res.ok) {
                        throw new Error(`HTTP error! status: ${res.status}`);
                    }
                    const data = await res.json();
                    setPoints(data);
                    console.log(data);
                } catch (error) {
                    console.error('There was a problem with the fetch operation:', error);
                }
            };
            fetchData();
        }
    }, [props.id, props.status]);

    const getMonthName = (monthNumber) => {
        const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        return monthNames[monthNumber - 1];
    };

    const options = {
        responsive: true,
        plugins: {
            legend: {
                display: false
            },
            datalabels: {
                color: 'black',
                anchor: 'end',
                align: 'top',
                font: {
                    size: 12,
                },
                formatter: function (value) {
                    return value;
                }
            }
        },
        scales: {
            x: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Month',
                    color: 'black',
                    font: {
                        size: 14,
                        weight: 'bold',
                    }
                },
                grid: {
                    color: 'rgba(0, 0, 0, 0.1)',
                },
                ticks: {
                    color: 'black',
                },
                border: {
                    color: 'black',
                    width: 2,
                }
            },
            y: {
                beginAtZero: true,
                suggestedMax: 25,
                title: {
                    display: true,
                    text: 'Total points',
                    color: 'black',
                    font: {
                        size: 14,
                        weight: 'bold',
                    }
                },
                grid: {
                    color: 'rgba(0, 0, 0, 0.1)',
                },
                ticks: {
                    color: 'black',
                },
                border: {
                    color: 'black',
                    width: 2,
                },
            }
        }
    };

    const data = {
        labels: [''].concat(Object.keys(points).map((month) => getMonthName(month.slice(0, 2)) + ' ' + month.slice(3, 7)), ['']),
        datasets: [
            {
                label: 'Points',
                data: [null].concat(Object.values(points), [null]),
                fill: false,
                backgroundColor: 'rgba(0, 0, 255, 1)',
                borderColor: 'rgba(0, 0, 255, 1)',
                borderWidth: 2,
                pointBackgroundColor: 'rgba(0, 0, 255, 1)',
                pointRadius: 5,
            }
        ]
    };

    return (
        <div className='component'>
            <h2>Monthly Points Completion</h2>
            <Line options={options} data={data} />
        </div>
    );
};
