import React, { useState, useEffect } from 'react';

const TeamRank = (props) => {

    // Retrieve API from server
    const [teamRanking, setTeam] = useState([]);

    useEffect(() => {
        if (props.status === 'login') {
            fetch(`/api/team/${props.id}/monthly_rank/${props.month}`)
                .then((res) => {
                    if (!res.ok) {
                        throw new Error(`HTTP error! status: ${res.status}`);
                    }
                    return res.json();
                })
                .then((data) => {
                    setTeam(data);
                    console.log(data);
                })
                .catch((error) => {
                    console.error('There was a problem with the fetch operation:', error);
                });
        }
    }, [props.id, props.month, props.status]);

    const getMonthName = (monthNumber) => {
        const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
        return monthNames[monthNumber - 1];
    };

    return (
        <div className='component'>
            <h2>Ranking in your team ({getMonthName(props.month.slice(0, 2)) + '/' + props.month.slice(3, 7)})</h2>
            {teamRanking.map((rank, index) => (
                <div key={index} style={{ display: 'flex', alignItems: 'center', padding: '10px', borderBottom: '1px solid #D3D3D3' }}>
                    <span>{rank.rank}</span>&nbsp;&nbsp;&nbsp;&nbsp;
                    {rank.status === 'up' ? (
                        <span style={{ marginLeft: '5px', fontSize: '20px', color: 'green' }}>▲</span>
                    ) : rank.status === 'down' ? (
                        <span style={{ marginLeft: '5px', fontSize: '20px', color: 'red' }}>▼</span>
                    ) : (
                        <span style={{ marginLeft: '5px', fontSize: '20px', color: 'black' }}>—</span>
                    )}&nbsp;&nbsp;&nbsp;&nbsp;
                    <span style={{ margin: '0 10px', fontWeight: 'bold' }}>{rank.name}</span>
                    <span style={{ marginLeft: 'auto' }}>{rank.points} points</span>
                </div>
            ))}
        </div>
    );
};

export default TeamRank;
