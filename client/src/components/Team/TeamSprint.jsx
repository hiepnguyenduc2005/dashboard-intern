import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
import { textTransform } from '@mui/system';

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
);

const TeamSprint = (props) => {
    // retrieve API from server
    const [dataSprint, setSprint] = useState({});
    if (props.status === 'login') {
        useEffect(() => {
            fetch(`/api/team/completion`)
                .then((res) => {
                    if (!res.ok) {
                        throw new Error(`HTTP error! status: ${res.status}`);
                    }
                    return res.json();
                })
                .then((data) => {
                    setSprint(data);
                    console.log(data);
                })
                .catch((error) => {
                    console.error('There was a problem with the fetch operation:', error);
                });
        }, []);
    }

    const getMonthName = (monthNumber) => {
        const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        return monthNames[monthNumber - 1];
    };

    const adminSprint = dataSprint['Admin Portal'] || {};
    const computeSprint = dataSprint['Compute'] || {};
    const dataFusionSprint = dataSprint['Data Fusion'] || {};

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
            }
        },
        scales: {
            x: {
                beginAtZero: true,
                title: {
                    display: false,
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
                title: {
                    display: false,
                },
                grid: {
                    color: 'rgba(0, 0, 0, 0.1)',
                },
                ticks: {
                    color: 'black',
                    callback: function(value) {
                        return `${value * 100}%`;
                    },
                    stepSize: 0.5,
                },
                border: {
                    color: 'black', 
                    width: 2,
                },
            }
        }
    };

    const data = {
        labels:  [''].concat(Object.keys(adminSprint).map((month) => getMonthName(month.slice(0, 2)) + ' ' + month.slice(3, 7)), ['']),
        datasets: [
            {
                label: 'Admin Portal',
                data: [null].concat(Object.values(adminSprint), [null]),
                fill: false,
                backgroundColor: 'rgba(0, 0, 255, 1)',
                borderColor: 'rgba(0, 0, 255, 1)',
                borderWidth: 2,
                pointBackgroundColor: 'rgba(0, 0, 255, 1)',
                pointRadius: 5,    
            }, 
            {
                label: 'Compute',
                data: [null].concat(Object.values(computeSprint), [null]),
                fill: false,
                backgroundColor: 'rgba(255, 127, 127, 1)',
                borderColor: 'rgba(255, 127, 127, 1)',
                borderWidth: 2,
                pointBackgroundColor: 'rgba(255, 127, 127, 1)',
                pointRadius: 5,    
            },
            {
                label: 'Data Fusion',
                data: [null].concat(Object.values(dataFusionSprint), [null]),
                fill: false,
                backgroundColor: 'rgba(0, 128, 0, 1)',
                borderColor: 'rgba(0, 128, 0, 1)',
                borderWidth: 2,
                pointBackgroundColor: 'rgba(0, 128, 0, 1)',
                pointRadius: 5,    
            },
        ]
    }

    return(
        <div className='component'>
            <h2>Monthly Sprint Completion Rate</h2>
            <Line options={options} data={data}/>
        </div>
    )
}

export default TeamSprint;
