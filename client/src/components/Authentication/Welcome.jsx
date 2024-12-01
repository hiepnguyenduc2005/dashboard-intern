const Welcome = ({user}) => {
    return(
        <div className='component'>
            <h2>Welcome</h2>
            <h4>Your name: </h4>
            <h5>{user.name}</h5>
            <h4>Your username: </h4>
            <h5>{user.username}</h5>
            <h4>Your team: </h4>
            <h5>{user.team}</h5>
        </div>
    )
}

export default Welcome;