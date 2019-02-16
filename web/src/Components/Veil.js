import React, {Component} from 'react';
import {withStyles} from '@material-ui/core/styles';


const styles = theme => ({
    root: {
        position: "absolute",
        top: 0,
        left: 0,
        width: "100%",
        height: "100%",
        opacity: ".5",
        background: "white",
    },
});


class Veil extends Component {

    render() {
        const {classes} = this.props;

        return (
            <div className={classes.root}>
                {this.props.children}
            </div>
        )
    }
}

export default withStyles(styles)(Veil);