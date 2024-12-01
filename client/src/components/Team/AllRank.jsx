import React, { useState, useEffect } from 'react';
import Avatar from '@mui/material/Avatar';

const AllRank = (props) => {

    // retrieve API from server
    const [allRanking, setAll] = useState([]);

    useEffect(() => {
        if (props.status === 'login') {
            fetch(`/api/team/monthly_rank/${props.month}`)
                .then((res) => {
                    if (!res.ok) {
                        throw new Error(`HTTP error! status: ${res.status}`);
                    }
                    return res.json();
                })
                .then((data) => {
                    setAll(data);
                    console.log(data);
                })
                .catch((error) => {
                    console.error('There was a problem with the fetch operation:', error);
                });
        }
    }, [props.month, props.status]);

    const getMonthName = (monthNumber) => {
        const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
        return monthNames[monthNumber - 1];
    };

    return (
        <div className='component'>
            <h2>FCI Performance Ranking ({getMonthName(props.month.slice(0, 2)) + '/' + props.month.slice(3, 7)})</h2>
            <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'flex-end', marginBottom: '20px' }}>
                {allRanking[1] && (
                    <div style={{ textAlign: 'center', marginRight: '20px' }}>
                        <Avatar src={allRanking[1].avatar} alt={allRanking[1].name} style={{ width: 60, height: 60, margin: '0 auto' }} />
                        <p style={{ fontWeight: 'bold', margin: '10px 0 5px' }}>{allRanking[1].name}</p>
                        <p style={{ margin: 0 }}>({allRanking[1].points} points)</p>
                        <div style={{ backgroundColor: '#0000FF', width: '80px', height: '120px', marginTop: '10px', color: '#fff', display: 'inline-block', alignContent: 'end', padding: '10px' }}>
                            <p style={{ margin: 0 }}>No.2</p>
                        </div>
                    </div>
                )}
                {allRanking[0] && (
                    <div style={{ textAlign: 'center', margin: '0 20px' }}>
                        <Avatar src={allRanking[0].avatar} alt={allRanking[0].name} style={{ width: 60, height: 60, margin: '0 auto' }} />
                        <p style={{ fontWeight: 'bold', margin: '10px 0 5px' }}>{allRanking[0].name}</p>
                        <p style={{ margin: 0 }}>({allRanking[0].points} points)</p>
                        <div style={{ backgroundColor: '#FF7F7F', width: '80px', height: '150px', marginTop: '10px', color: '#fff', display: 'inline-block', alignContent: 'end', padding: '10px' }}>
                            <p style={{ margin: 0 }}>No.1</p>
                        </div>
                    </div>
                )}
                {allRanking[2] && (
                    <div style={{ textAlign: 'center', marginLeft: '20px' }}>
                        <Avatar src={allRanking[2].avatar} alt={allRanking[2].name} style={{ width: 60, height: 60, margin: '0 auto' }} />
                        <p style={{ fontWeight: 'bold', margin: '10px 0 5px' }}>{allRanking[2].name}</p>
                        <p style={{ margin: 0 }}>({allRanking[2].points} points)</p>
                        <div style={{ backgroundColor: '#008000', width: '80px', height: '90px', marginTop: '10px', color: '#fff', display: 'inline-block', alignContent: 'end', padding: '10px' }}>
                            <p style={{ margin: 0 }}>No.3</p>
                        </div>
                    </div>
                )}
            </div>
            {allRanking.slice(3).map((rank, index) => (
                <div key={index} style={{ display: 'flex', alignItems: 'center', padding: '10px', borderBottom: '1px solid #D3D3D3' }}>
                    <span>{index + 4}</span>&nbsp;&nbsp;&nbsp;&nbsp;
                    <Avatar src={rank.avatar} alt={rank.name} />&nbsp;&nbsp;&nbsp;&nbsp;
                    <span style={{ margin: '0 10px', fontWeight: 'bold' }}>{rank.name}</span>
                    <span style={{ marginLeft: 'auto' }}>{rank.points} points</span>
                </div>
            ))}
        </div>
    );
}

export default AllRank;
