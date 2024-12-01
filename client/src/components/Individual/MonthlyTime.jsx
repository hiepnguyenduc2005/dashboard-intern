import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
);

export const MonthlyTime = (props) => {
    const [dataTime, setTime] = useState([]);

    useEffect(() => {
        if (props.status === 'login') {
            const fetchData = async () => {
                try {
                    const res = await fetch(`/api/individual/${props.id}/monthly_time`);
                    if (!res.ok) {
                        throw new Error(`HTTP error! status: ${res.status}`);
                    }
                    const data = await res.json();
                    setTime(data);
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
                display: true,
                position: 'bottom',
                labels: {
                    usePointStyle: true,
                    pointStyle: 'circle',
                },
            },
            datalabels: {
                display: false,
            },
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
                    },
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
            },
            y: {
                beginAtZero: true,
                suggestedMax: 20,
                title: {
                    display: true,
                    text: 'Time (hours)',
                    color: 'black',
                    font: {
                        size: 14,
                        weight: 'bold',
                    },
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
            },
        },
    };

    const data = {
        labels: [''].concat(Object.keys(dataTime).map((month) => getMonthName(month.slice(0, 2)) + ' ' + month.slice(3, 7)), ['']),
        datasets: [
            {
                label: '1 point task',
                data: [null].concat(Object.values(dataTime).map((month) => month['1pt_time']), [null]),
                fill: false,
                backgroundColor: 'rgba(0, 0, 255, 1)',
                borderColor: 'rgba(0, 0, 255, 1)',
                borderWidth: 2,
                pointBackgroundColor: 'rgba(0, 0, 255, 1)',
                pointRadius: 5,
            },
            {
                label: '2 point task',
                data: [null].concat(Object.values(dataTime).map((month) => month['2pt_time']), [null]),
                fill: false,
                backgroundColor: 'rgba(255, 127, 127, 1)',
                borderColor: 'rgba(255, 127, 127, 1)',
                borderWidth: 2,
                pointBackgroundColor: 'rgba(255, 127, 127, 1)',
                pointRadius: 5,
            },
            {
                label: '3 point task',
                data: [null].concat(Object.values(dataTime).map((month) => month['3pt_time']), [null]),
                fill: false,
                backgroundColor: 'rgba(0, 128, 0, 1)',
                borderColor: 'rgba(0, 128, 0, 1)',
                borderWidth: 2,
                pointBackgroundColor: 'rgba(0, 128, 0, 1)',
                pointRadius: 5,
            },
        ],
    };

    return (
        <div className='component'>
            <h2>Monthly Task Completion Time</h2>
            <Line options={options} data={data} />
        </div>
    );
};
