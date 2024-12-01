import React, { useState, useEffect } from 'react';
import './Level.css';

export const Level = (props) => {
    const [score, setScore] = useState(0);
    const [maxScore, setMaxScore] = useState(1);

    useEffect(() => {
        if (props.status === 'login') {
            fetch(`/api/individual/${props.id}/level`)
                .then((res) => {
                    if (!res.ok) {
                        throw new Error(`HTTP error! status: ${res.status}`);
                    }
                    return res.json();
                })
                .then((data) => {
                    setScore(data.point); // Move setScore inside the then block
                    setMaxScore(data.max_score); // Move setMaxScore inside the then block
                    console.log(data);
                })
                .catch((error) => {
                    console.error('There was a problem with the fetch operation:', error);
                });
        }
    }, [props.status, props.id]); // Add props.status and props.id to the dependency array

    const progress = (score / maxScore) * 100;

    const levels = ['Fresher', 'Junior', 'Senior', 'Expert'];
    const levelPositions = [0, 33, 67, 100];

    return (
        <>
            <h2>Level progression</h2>
            <div className="progress-container">
                <div className="progress-bar">
                    <div className="progress-line-container">
                        <div className="progress-line-background"></div>
                        <div className="progress-line" style={{ width: `${progress}%` }}></div>
                    </div>
                    {levels.map((level, index) => (
                        <div
                            key={level}
                            className="level-container"
                            style={{ left: `${levelPositions[index]}%` }}
                        >
                            <div
                                className={`level-icon ${
                                    progress >= levelPositions[index] ? 'active' : ''
                                }`}
                            >
                                <span className="level-star">★</span>
                            </div>
                            <span className="level-label">{level}</span>
                        </div>
                    ))}
                </div>
            </div>
        </>
    );
};
