import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Filler, Legend } from 'chart.js';

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Filler,
    Legend,
);

export const SprintPoints = (props) => {
    const [dataSprints, setSprints] = useState([]);

    useEffect(() => {
        if (props.status === 'login') {
            const fetchData = async () => {
                try {
                    const res = await fetch(`/api/individual/${props.id}/sprint_pts`);
                    if (!res.ok) {
                        throw new Error(`HTTP error! status: ${res.status}`);
                    }
                    const data = await res.json();
                    setSprints(data);
                    console.log(data);
                } catch (error) {
                    console.error('There was a problem with the fetch operation:', error);
                }
            };
            fetchData();
        }
    }, [props.id, props.status]);

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
                reverse: true,
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
                    text: 'Sprint',
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
                suggestedMax: 10,
                title: {
                    display: true,
                    text: 'Points',
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
        labels: [''].concat(Object.keys(dataSprints), ['']),
        datasets: [
            {
                label: 'Points assigned but not completed',
                data: [null].concat(Object.values(dataSprints).map((sprint) => sprint['incomplete']), [null]),
                fill: true,
                backgroundColor: 'rgba(255, 127, 127, 0.2)',
                borderColor: 'rgba(255, 127, 127, 1)',
                borderWidth: 2,
                pointBackgroundColor: 'rgba(255, 127, 127, 1)',
                pointRadius: 0,
            },
            {
                label: 'Points completed',
                data: [null].concat(Object.values(dataSprints).map((sprint) => sprint['completed']), [null]),
                fill: true,
                backgroundColor: 'rgba(0, 0, 255, 0.2)',
                borderColor: 'rgba(0, 0, 255, 1)',
                borderWidth: 2,
                pointBackgroundColor: 'rgba(0, 0, 255, 1)',
                pointRadius: 0,
            },
        ],
    };

    return (
        <div className='component'>
            <h2>Sprint Points Breakdown: Achieved vs. Outstanding</h2>
            <Line options={options} data={data} />
        </div>
    );
};
