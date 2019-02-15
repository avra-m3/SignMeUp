import React, {Component} from 'react';
import * as PropTypes from "prop-types";
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
import Radio from '@material-ui/core/Radio';
import RadioGroup from '@material-ui/core/RadioGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import FormControl from '@material-ui/core/FormControl';
import FormLabel from '@material-ui/core/FormLabel';
import config from './config'
import {withStyles} from '@material-ui/core/styles';
import {handleFetchErrors} from "./utils";
import Icon from "@material-ui/core/Icon";
import Button from "@material-ui/core/Button";


const styles = theme => ({
    root: {
        display: 'flex',
        flexDirection: 'column',
        maxWidth: "300px",
        margin: "auto"

    },
    formControl: {
        margin: theme.spacing.unit * 3,
    },
    group: {
        margin: `${theme.spacing.unit}px 0`,
    },
    button: {
        margin: theme.spacing.unit,
    },
    rightIcon: {
        marginLeft: theme.spacing.unit,
    },

});


class ClubSelector extends Component {

    state = {
        available: null,
        selected: undefined
    };

    static propTypes = {
        callback: PropTypes.func.isRequired,
        authorization: PropTypes.string.isRequired,
        deauthorizationCallback: PropTypes.func.isRequired,
    };

    componentDidMount() {
        fetch(`${config.api}${config.endpoints.clubs}`, {
            headers: new Headers({
                Authorization: this.props.authorization
            })
        }).then(handleFetchErrors).then(data => {
            this.setState({
                available: data.data,
                selected: data.data.length > 0 ? data.data[0].name : undefined
            })
        }).catch((err) => {
            console.log(err);
            if (err.message === "401") {
                console.log("Request DeAuth (401)");
                this.props.deauthorizationCallback();
            }
            this.setState({
                available: undefined
            })
        })
    }

    render() {
        const {classes} = this.props;

        const isLoadingClubs = this.state.available === null;
        const isLoadingClubsErred = this.state.available === undefined;
        const clubs = this.state.available;


        return (
            <Paper>
                {
                    isLoadingClubs ? <div>
                            <Typography variant="headline" elevation={4}>Loading...</Typography>
                        </div> :
                        isLoadingClubsErred ?
                            <Typography variant="headline" elevation={4}>Could not load clubs (Unknown
                                error)</Typography> :
                            <div className={classes.root}>
                                <FormControl component="fieldset" className={classes.formControl}>
                                    <FormLabel component="legend">Clubs</FormLabel>
                                    <RadioGroup
                                        aria-label="Clubs"
                                        name="clubs"
                                        className={classes.group}
                                        value={this.state.selected}
                                        onChange={this.selectClub}
                                    >
                                        {clubs.map(club => {
                                            return (
                                                <FormControlLabel value={club.name} control={<Radio/>}
                                                                  label={club.name}/>)

                                        })}
                                    </RadioGroup>
                                </FormControl>
                                <Button variant="contained" color="primary" className={classes.button}
                                        onClick={event => this.props.callback(this.state.selected)}>
                                    Continue
                                    <Icon className={classes.rightIcon}>send</Icon>
                                </Button>
                            </div>
                }
            </Paper>
        )
    }

    selectClub = event => {
        this.setState({
            selected: event.target.value
        })
    }
}

export default withStyles(styles)(ClubSelector);