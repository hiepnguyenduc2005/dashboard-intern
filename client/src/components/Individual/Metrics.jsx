import React, { useState, useEffect } from 'react';
import CheckCircleIcon from '@mui/icons-material/CheckCircle'; 
import StarIcon from '@mui/icons-material/Star';
import StarHalfIcon from '@mui/icons-material/StarHalf';
import StarOutlineIcon from '@mui/icons-material/StarOutline';

export const Metrics = (props) => {
    
    const [metrics, setMetrics] = useState({
        point: 0,
        rank: 0,
        total: 0,
        completion_rate: 0,
        average_peer_rating: 0
    });

    useEffect(() => {
        if (props.status === 'login') {
            fetch(`/api/individual/${props.id}/metrics`)
                .then((res) => {
                    if (!res.ok) {
                        throw new Error(`HTTP error! status: ${res.status}`);
                    }
                    return res.json();
                })
                .then((data) => {
                    setMetrics(data);
                    console.log(data);
                })
                .catch((error) => {
                    console.error('There was a problem with the fetch operation:', error);
                });
        }
    }, [props.status, props.id]); // Ensure the effect runs when id or status changes

    const { point, rank, total, completion_rate, average_peer_rating } = metrics;
    const validPeer = typeof average_peer_rating === 'number' && !isNaN(average_peer_rating) ? average_peer_rating : 0;
    const fullStars = Math.floor(validPeer);
    const halfStar = average_peer_rating % 1 !== 0;
    const emptyStars = 5 - fullStars - (halfStar ? 1 : 0);

    return (
        <>  
            <div className='component'>
                <h2>Experience Points</h2>
                <h3>{point}&nbsp;<CheckCircleIcon style={{ color: '#20C997', fontSize: '24px' }} /></h3>
            </div>
            <div className='component'>
                <h2>Rank</h2>
                <h3>{rank}/{total}&nbsp;<CheckCircleIcon style={{ color: '#20C997', fontSize: '24px' }} /></h3>
            </div>
            <div className='component'>
                <h2>Completion rate</h2>
                <h3>{(completion_rate * 100).toFixed(2)}%&nbsp;<CheckCircleIcon style={{ color: '#20C997', fontSize: '24px' }} /></h3>
            </div>
            <div className='component'>
                <h2>Month avg. peer rating</h2>
                <h3>
                    {Array(fullStars).fill().map((_, i) => <StarIcon key={i} style={{ color: '#f5a623' }} />)}
                    {halfStar && <StarHalfIcon style={{ color: '#f5a623' }} />}
                    {Array(emptyStars).fill().map((_, i) => <StarOutlineIcon key={i} style={{ color: '#f5a623' }} />)}
                </h3>
             </div>   
        </>
    );
};
