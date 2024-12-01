import React from 'react';
import AllRank from './Team/AllRank';
import TeamRank from './Team/TeamRank';
import TeamSprint from './Team/TeamSprint';

const Team = (props) => {
    return (
        <>
        <div className='heading'>
                <h1>FCI Peformance Dashboard</h1>
        </div>
        <div className='subhead grid2'>
            <AllRank month={props.month} status={props.status}/>
            <div>
                <TeamRank id={props.id} month={props.month} status={props.status}/>
                <TeamSprint status={props.status}/>
            </div>
        </div>
        </>
    )
};

export default Team;