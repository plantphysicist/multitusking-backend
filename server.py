# server.py

import Config
import game_logic as util
import time
import random
import math

# TODO JS does SQL & HTML stuff here

# TODO needs a name
class NeedsName:
    def __init__(self):
        self.users = []
        self.mass_food = []
        self.food = []
        self.virus = []
        self.sockets = {}
        # TODO: Solve this quadtree nonesense
        self.tree = None # quadtree(0, 0, Config.Game.gameWidth, Config.Game.GAME_HEIGHT);

        # TODO: How do collision ;-;
        self.sat = None # require('sat');

        # TODO i cri
        self.V = None #SAT.Vector;
        self.C = None #SAT.Circle;

        self.init_mass_log = util.log(Config.Game.DEFAULT_PLAYER_MASS, Config.Game.SLOW_BASE)

    def add_food(self, to_add):
        """[summary]

        Args:
            to_add ([type]): [description]
        """
        radius = util.mass_to_radius(Config.Game.FOOD_MASS)

        for _ in range(to_add):
            if Config.Game.FOOD_UNIFORM_DISPOSITION:
                position = util.uniform_position(self.food, radius)
            else:
                position = util.random_position(radius)

            self.food.append(
                {
                    'id': int('{}{}'.format(time.time_ns(), len(self.food))),
                    'x': position['x'],
                    'y': position['y'],
                    'radius': radius,
                    'mass': random.random() + 2,
                    'hue': round(random.random() * 360)
                }
            )

    def add_virus(self, to_add):
        for _ in range(to_add):
            mass = util.random_in_range(Config.Virus.DEFAULT_MASS_FROM, Config.Virus.DEFAULT_MASS_TO)
            radius = util.mass_to_radius(mass)
            if Config.Game.VIRUS_UNIFORM_DISPOSITION:
                position = util.uniform_position(self.virus, radius)
            else:
                position = util.random_position(radius)
            
            self.virus.append(
                {
                    'id': int('{}{}'.format(time.time_ns(), len(self.virus))),
                    'x': position['x'],
                    'y': position['y'],
                    'radius': radius,
                    'mass': mass,
                    'fill': Config.Virus.FILL,
                    'stroke': Config.Virus.STROKE,
                    'stroke_width': Config.Virus.STROKE_WIDTH
                }
            )

    def remove_food(self, to_rem):
        for _ in range(to_rem):
            self.food.pop()

    def move_player(self, player):
        x = 0
        y = 0
        for i in range(len(player.cells)):
            target = {
                'x': player.x - player.cells[i].x + player.target.x,
                'y': player.y - player.cells[i].y + player.target.y
            }
            dist = sqrt(target['y'] ** 2 + target.x ** 2)
            deg = math.atan2(target['y'], target['x'])
            slow_down = 1
            if player.cells[i].speed <= 6.25:
                slow_down = util.log(player.cells[i].mass, Config.Game.SLOW_BASE) - self.init_mass_log - 1

            delta_y = player.cells[i].speed * math.sin(deg) / slow_down
            delta_x = player.cells[i].speed * math.cos(deg) / slow_down

            if player.cells[i].speed > 6.25:
                player.cells[i].speed -= 0.5

            if dist < (50 + player.cells[i].radius):
                delta_y *= dist / (50 + player.cells[i].radius)
                delta_x *= dist / (50 + player.cells[i].radius)

            player.cells[i].y += delta_y
            player.cells[i].x += delta_x

            # TODO Find best solution.
            for j in range(len(player.cells)):
                if j != i and player.cells[i]:
                    distance = sqrt((player.cells[j].y - player.cells[i].y) ** 2)
                               + (player.cells[j].x - player.cells[i].x) ** 2
                    radius_total = player.cells[i].radius + player.cells[j].radius
                    if distance < radius_total:
                        if player.last_split >  time.time_ns() - 1000 * Config.Game.MERGE_TIMER:
                            if player.cells[i].x < player.cells[j].x:
                                player.cells[i].x -= 1
                        elif player.cells[i].x > player.cells[j].x:
                            player.cells[i].x += 1
                        
                        if player.cells[i].y < player.cells[j].y:
                            player.cells[i].y -= 1
                        
                        elif player.cells[i].y > player.cells[j].y:
                            player.cells[i].y += 1
                    

                    elif distance < radius_total / 1.75:
                        player.cells[i].mass += player.cells[j].mass
                        player.cells[i].radius = util.mass_to_radius(player.cells[i].mass)
                        del player.cells[j]

        if len(player.cells) > i:
            border_calc = player.cells[i].radius / 3
            if player.cells[i].x > Config.Game.GAME_WIDTH - border_calc:
                player.cells[i].x = Config.Game.GAME_WIDTH - border_calc

            if player.cells[i].y > Config.Game.GAME_HEIGHT - border_calc:
                player.cells[i].y = Config.Game.GAME_HEIGHT - border_calc

            if player.cells[i].x < border_calc:
                player.cells[i].x = border_calc

            if player.cells[i].y < border_calc:
                player.cells[i].y = border_calc

            x += player.cells[i].x
            y += player.cells[i].y
    player.x = x / len(player.cells)
    player.y = y / len(player.cells)

    def move_mass(self, mass):
    deg = math.atan2(mass.target.y, mass.target.x);
    delta_y = mass.speed * math.sin(deg)
    delta_x = mass.speed * math.cos(deg)

    mass.speed -= 0.5
    if mass.speed < 0:
        mass.speed = 0
    
    if not math.isnan(delta_y):
        mass.y += delta_y

    if not math.isnan(delta_x):
        mass.x += delta_x

    border_calc = mass.radius + 5

    if mass.x > Config.Game.GAME_WIDTH - border_calc:
        mass.x = Config.Game.GAME_WIDTH - border_calc

    if mass.y > Config.Game.GAME_HEIGHT - border_calc:
        mass.y = Config.Game.GAME_HEIGHT - border_calc

    if mass.x < border_calc:
        mass.x = border_calc

    if mass.y < border_calc:
        mass.y = border_calc


    def balance_mass(self):
        total_mass = len(self.food) * Config.Game.FOOD_MASS + [ u.mass_total for u in self.users ].sum()

        mass_diff = Config.Game.GAME_MASS - total_mass
        max_food_diff = Config.Game.MAX_FOOD - len(food)
        food_diff = int(mass_diff / Config.Game.FOOD_MASS) - max_food_diff
        food_to_add = min(food_diff, max_food_diff)
        food_to_remove = -1 * max(food_diff, max_food_diff)

        if food_to_add > 0:
            #console.log('[DEBUG] Adding ' + food_to_add + ' food to level!');
            self.add_food(food_to_add)
            #console.log('[DEBUG] Mass rebalanced!');

        elif food_to_remove > 0:
            #console.log('[DEBUG] Removing ' + food_to_remove + ' food from level!');
            self.remove_food(food_to_remove)
            #console.log('[DEBUG] Mass rebalanced!');


        virus_to_add = Config.Game.MAX_VIRUS - len(self.virus)

        if virus_to_add > 0:
            add_virus(virus_to_add)


io.on('connection', function (socket) {
    console.log('A user connected!', socket.handshake.query.type);

    var type = socket.handshake.query.type;
    var radius = util.mass_to_radius(Config.Game.defaultPlayerMass);
    var position = Config.Game.newPlayerInitialPosition == 'farthest' ? util.uniformPosition(users, radius) : util.randomPosition(radius);

    var cells = [];
    var mass_total = 0;
    if(type === 'player') {
        cells = [{
            mass: Config.Game.defaultPlayerMass,
            x: position.x,
            y: position.y,
            radius: radius
        }];
        mass_total = Config.Game.defaultPlayerMass;
    }

    var current_player = {
        id: socket.id,
        x: position.x,
        y: position.y,
        w: Config.Game.defaultPlayerMass,
        h: Config.Game.defaultPlayerMass,
        cells: cells,
        mass_total: mass_total,
        hue: Math.round(Math.random() * 360),
        type: type,
        last_heartbeat: new Date().getTime(),
        target: {
            x: 0,
            y: 0
        }
    };

    socket.on('gotit', function (player) {
        console.log('[INFO] Player ' + player.name + ' connecting!');

        if (util.find_index(users, player.id) > -1) {
            console.log('[INFO] Player ID is already connected, kicking.');
            socket.disconnect();
        } else if (!util.validNick(player.name)) {
            socket.emit('kick', 'Invalid username.');
            socket.disconnect();
        } else {
            console.log('[INFO] Player ' + player.name + ' connected!');
            sockets[player.id] = socket;

            var radius = util.mass_to_radius(Config.Game.defaultPlayerMass);
            var position = Config.Game.newPlayerInitialPosition == 'farthest' ? util.uniformPosition(users, radius) : util.randomPosition(radius);

            player.x = position.x;
            player.y = position.y;
            player.target.x = 0;
            player.target.y = 0;
            if(type === 'player') {
                player.cells = [{
                    mass: Config.Game.defaultPlayerMass,
                    x: position.x,
                    y: position.y,
                    radius: radius
                }];
                player.mass_total = Config.Game.defaultPlayerMass;
            }
            else {
                 player.cells = [];
                 player.mass_total = 0;
            }
            player.hue = Math.round(Math.random() * 360);
            current_player = player;
            current_player.last_heartbeat = new Date().getTime();
            users.push(current_player);

            io.emit('playerJoin', { name: current_player.name });

            socket.emit('gameSetup', {
                gameWidth: Config.Game.gameWidth,
                gameHeight: Config.Game.gameHeight
            });
            console.log('Total players: ' + users.length);
        }

    });

    socket.on('pingcheck', function () {
        socket.emit('pongcheck');
    });

    socket.on('windowResized', function (data) {
        current_player.screenWidth = data.screenWidth;
        current_player.screenHeight = data.screenHeight;
    });

    socket.on('respawn', function () {
        if (util.find_index(users, current_player.id) > -1)
            users.splice(util.find_index(users, current_player.id), 1);
        socket.emit('welcome', current_player);
        console.log('[INFO] User ' + current_player.name + ' respawned!');
    });

    socket.on('disconnect', function () {
        if (util.find_index(users, current_player.id) > -1)
            users.splice(util.find_index(users, current_player.id), 1);
        console.log('[INFO] User ' + current_player.name + ' disconnected!');

        socket.broadcast.emit('playerDisconnect', { name: current_player.name });
    });

    socket.on('playerChat', function(data) {
        var _sender = data.sender.replace(/(<([^>]+)>)/ig, '');
        var _message = data.message.replace(/(<([^>]+)>)/ig, '');
        if (Config.Game.logChat === 1) {
            console.log('[CHAT] [' + (new Date()).getHours() + ':' + (new Date()).getMinutes() + '] ' + _sender + ': ' + _message);
        }
        socket.broadcast.emit('serverSendPlayerChat', {sender: _sender, message: _message.substring(0,35)});
    });

    socket.on('pass', function(data) {
        if (data[0] === Config.Game.adminPass) {
            console.log('[ADMIN] ' + current_player.name + ' just logged in as an admin!');
            socket.emit('serverMSG', 'Welcome back ' + current_player.name);
            socket.broadcast.emit('serverMSG', current_player.name + ' just logged in as admin!');
            current_player.admin = true;
        } else {
            
            // TODO: Actually log incorrect passwords.
              console.log('[ADMIN] ' + current_player.name + ' attempted to log in with incorrect password.');
              socket.emit('serverMSG', 'Password incorrect, attempt logged.');
             pool.query('INSERT INTO logging SET name=' + current_player.name + ', reason="Invalid login attempt as admin"');
        }
    });

    socket.on('kick', function(data) {
        if (current_player.admin) {
            var reason = '';
            var worked = false;
            for (var e = 0; e < users.length; e++) {
                if (users[e].name === data[0] && !users[e].admin && !worked) {
                    if (data.length > 1) {
                        for (var f = 1; f < data.length; f++) {
                            if (f === data.length) {
                                reason = reason + data[f];
                            }
                            else {
                                reason = reason + data[f] + ' ';
                            }
                        }
                    }
                    if (reason !== '') {
                       console.log('[ADMIN] User ' + users[e].name + ' kicked successfully by ' + current_player.name + ' for reason ' + reason);
                    }
                    else {
                       console.log('[ADMIN] User ' + users[e].name + ' kicked successfully by ' + current_player.name);
                    }
                    socket.emit('serverMSG', 'User ' + users[e].name + ' was kicked by ' + current_player.name);
                    sockets[users[e].id].emit('kick', reason);
                    sockets[users[e].id].disconnect();
                    users.splice(e, 1);
                    worked = true;
                }
            }
            if (!worked) {
                socket.emit('serverMSG', 'Could not locate user or user is an admin.');
            }
        } else {
            console.log('[ADMIN] ' + current_player.name + ' is trying to use -kick but isn\'t an admin.');
            socket.emit('serverMSG', 'You are not permitted to use this command.');
        }
    });

    // Heartbeat function, update everytime.
    socket.on('0', function(target) {
        current_player.last_heartbeat = new Date().getTime();
        if (target.x !== current_player.x || target.y !== current_player.y) {
            current_player.target = target;
        }
    });

    socket.on('1', function() {
        // Fire food.
        for(var i=0; i<current_player.cells.length; i++)
        {
            if(((current_player.cells[i].mass >= Config.Game.defaultPlayerMass + Config.Game.fireFood) && Config.Game.fireFood > 0) || (current_player.cells[i].mass >= 20 && Config.Game.fireFood === 0)){
                var mass = 1;
                if(Config.Game.fireFood > 0)
                    mass = Config.Game.fireFood;
                else
                    mass = current_player.cells[i].mass*0.1;
                current_player.cells[i].mass -= mass;
                current_player.mass_total -=mass;
                mass_food.push({
                    id: current_player.id,
                    num: i,
                    mass: mass,
                    hue: current_player.hue,
                    target: {
                        x: current_player.x - current_player.cells[i].x + current_player.target.x,
                        y: current_player.y - current_player.cells[i].y + current_player.target.y
                    },
                    x: current_player.cells[i].x,
                    y: current_player.cells[i].y,
                    radius: util.mass_to_radius(mass),
                    speed: 25
                });
            }
        }
    });
    socket.on('2', function(virusCell) {
        function splitCell(cell) {
            if(cell && cell.mass && cell.mass >= Config.Game.defaultPlayerMass*2) {
                cell.mass = cell.mass/2;
                cell.radius = util.mass_to_radius(cell.mass);
                current_player.cells.push({
                    mass: cell.mass,
                    x: cell.x,
                    y: cell.y,
                    radius: cell.radius,
                    speed: 25
                });
            }
        }

        if(current_player.cells.length < Config.Game.limitSplit && current_player.mass_total >= Config.Game.defaultPlayerMass*2) {
            //Split single cell from virus
            if(virusCell) {
              splitCell(current_player.cells[virusCell]);
            }
            else {
              //Split all cells
              if(current_player.cells.length < Config.Game.limitSplit && current_player.mass_total >= Config.Game.defaultPlayerMass*2) {
                  var numMax = current_player.cells.length;
                  for(var d=0; d<numMax; d++) {
                      splitCell(current_player.cells[d]);
                  }
              }
            }
            current_player.lastSplit = new Date().getTime();
        }
    });
});

    def tick_player(self, current_player):
        if current_player.last_heartbeat < time.ctime() - Config.Game.MAX_HEARTBEAT_INTERVAL:
            self.sockets[current_player.id].emit('kick', 'Last heartbeat received over ' + Config.Game.MAX_HEARTBEAT_INTERVAL + ' ago.') # TODO does emit work the same here>
            self.sockets[current_player.id].disconnect() # TODO does this function work like that?
        }

        move_player(current_player)

        def func_food(f):
            return SAT.pointInCircle(new V(f.x, f.y), player_circle) # TODO how does SAT translate to python?

        def delete_food(f):
            self.food[f] = {}
            del self.food[f]

        def eat_mass(m):
            if SAT.pointInCircle(new V(m.x, m.y), player_circle)): # TODO how does SAT translate to python?
                if m.id == current_player.id and m.speed > 0 and z == m.num
                    return False
                if current_cell.mass > m.mass * 1.1
                    return True

            return False


        def check(user):
            for i in range(len(user.cells)):
                if user.cells[i].mass > 10 and user.id != current_player.id:
                    response = new SAT.Response() # TODO how does SAT translate to python?
                    var collided = SAT.testCircleCircle(player_circle, # TODO how does SAT translate to python?
                        new C(new V(user.cells[i].x, user.cells[i].y), user.cells[i].radius),# TODO how does SAT translate to python?
                        response);# TODO how does SAT translate to python?
                    if collided:
                        response.aUser = current_cell # TODO what's going on here fml
                        response.bUser = {
                            id: user.id,
                            name: user.name,
                            x: user.cells[i].x,
                            y: user.cells[i].y,
                            num: i,
                            mass: user.cells[i].mass
                        };
                        player_collisions.append(response)
                    }
                }
            }
            return True
        }

        def collision_check(collision):
            if collision.aUser.mass > collision.bUser.mass * 1.1  
                and collision.aUser.radius > sqrt((collision.aUser.x - collision.bUser.x) **  2) + (collision.aUser.y - collision.bUser.y) ** 2) * 1.75):
                print('[DEBUG] Killing user: ' + collision.bUser.id)
                print('[DEBUG] Collision info:')
                print(collision)

                num_user = util.find_index(self.users, collision.bUser.id)
                if num_user > -1:
                    if len(self.users[num_user].cells) > 1:
                        self.users[num_user].mass_total -= collision.bUser.mass
                        del self.users[num_user].cells.splice[collision.bUser.num]
                    else:
                        del self.users[num_user]
                        io.emit('playerDied', { name: collision.bUser.name }) # TODO fix this io.emit thingy?
                        self.sockets[collision.bUser.id].emit('RIP') # TODO fix this io.emit thingy?

                current_player.mass_total += collision.bUser.mass
                collision.aUser.mass += collision.bUser.mass

        for z in range(len(current_player.cells)):
            current_cell = current_player.cells[z]
            player_circle = new C( # TODO what is this
                new V(current_cell.x, current_cell.y),
                current_cell.radius
            )

            food_eaten = food.map(func_food)
                .reduce( function(a, b, c) { return b ? a.concat(c) : a; }, []); # TODO figure this one out

            for f in food_eaten:
                delete_food(f)

            mass_eaten = mass_food.map(eat_mass)
                .reduce(function(a, b, c) {return b ? a.concat(c) : a; }, []); # TODO figure this one out

            virus_collision = virus.map(func_food)
            .reduce( function(a, b, c) { return b ? a.concat(c) : a; }, []); # TODO figure this one out

            if(virus_collision > 0 and current_cell.mass > virus[virus_collision].mass:
                self.sockets[current_player.id].emit('virusSplit', z); # TODO fix this io.emit thingy?
                del self.virus[virus_collision]
            }

            gained_mass = 0
            for m in range(len(mass_eaten)):
                gained_mass += mass_food[mass_eaten[m]].mass
                mass_food[mass_eaten[m]] = {}
                del mass_food[mass_eaten[m]]
                for n in range(len(mass_eaten)):
                    if mass_eaten[m] < mass_eaten[n]:
                        mass_eaten[n]--

            if not current_cell.speed:
                current_cell.speed = 6.25
            gained_mass += (food_eaten.length * Config.Game.FOOD_MASS)
            current_cell.mass += gained_mass
            current_player.mass_total += gained_mass
            current_cell.radius = util.mass_to_radius(current_cell.mass)
            player_circle.r = current_cell.radius

            self.tree.clear()
            foreach u in self.users.forEach:
                self.tree.put(u)
            player_collisions = []

            other_users =  self.tree.get(current_player, check)

            foreach p in player_collisions:
                collision_check(p)

    def move_loop(self):
        for u in self.users:
            self.tick_player(u)

        for m in self.mass_food:
            if m.speed > 0:
                move_mass(m)

def game_loop(self):
    if len(self.users) > 0:
        self.users.sort( function(a, b) { return b.mass_total - a.mass_total; }); # TODO figure this one out

        top_users = []

        for var i = 0; i < Math.min(10, users.length); i++) {
            if(users[i].type == 'player') {
                topUsers.push({
                    id: users[i].id,
                    name: users[i].name
                });
            }
        }
        if (isNaN(leaderboard) || leaderboard.length !== topUsers.length) {
            leaderboard = topUsers;
            leaderboardChanged = true;
        }
        else {
            for (i = 0; i < leaderboard.length; i++) {
                if (leaderboard[i].id !== topUsers[i].id) {
                    leaderboard = topUsers;
                    leaderboardChanged = true;
                    break;
                }
            }
        }
        for (i = 0; i < users.length; i++) {
            for(var z=0; z < users[i].cells.length; z++) {
                if (users[i].cells[z].mass * (1 - (Config.Game.massLossRate / 1000)) > Config.Game.defaultPlayerMass && users[i].mass_total > Config.Game.minMassLoss) {
                    var massLoss = users[i].cells[z].mass * (1 - (Config.Game.massLossRate / 1000));
                    users[i].mass_total -= users[i].cells[z].mass - massLoss;
                    users[i].cells[z].mass = massLoss;
                }
            }
        }
    }
    balanceMass();
}

function sendUpdates() {
    users.forEach( function(u) {
        // center the view if x/y is undefined, this will happen for spectators
        u.x = u.x || Config.Game.gameWidth / 2;
        u.y = u.y || Config.Game.gameHeight / 2;

        var visibleFood  = food
            .map(function(f) {
                if ( f.x > u.x - u.screenWidth/2 - 20 &&
                    f.x < u.x + u.screenWidth/2 + 20 &&
                    f.y > u.y - u.screenHeight/2 - 20 &&
                    f.y < u.y + u.screenHeight/2 + 20) {
                    return f;
                }
            })
            .filter(function(f) { return f; });

        var visibleVirus  = virus
            .map(function(f) {
                if ( f.x > u.x - u.screenWidth/2 - f.radius &&
                    f.x < u.x + u.screenWidth/2 + f.radius &&
                    f.y > u.y - u.screenHeight/2 - f.radius &&
                    f.y < u.y + u.screenHeight/2 + f.radius) {
                    return f;
                }
            })
            .filter(function(f) { return f; });

        var visibleMass = mass_food
            .map(function(f) {
                if ( f.x+f.radius > u.x - u.screenWidth/2 - 20 &&
                    f.x-f.radius < u.x + u.screenWidth/2 + 20 &&
                    f.y+f.radius > u.y - u.screenHeight/2 - 20 &&
                    f.y-f.radius < u.y + u.screenHeight/2 + 20) {
                    return f;
                }
            })
            .filter(function(f) { return f; });

        var visibleCells  = users
            .map(function(f) {
                for(var z=0; z<f.cells.length; z++)
                {
                    if ( f.cells[z].x+f.cells[z].radius > u.x - u.screenWidth/2 - 20 &&
                        f.cells[z].x-f.cells[z].radius < u.x + u.screenWidth/2 + 20 &&
                        f.cells[z].y+f.cells[z].radius > u.y - u.screenHeight/2 - 20 &&
                        f.cells[z].y-f.cells[z].radius < u.y + u.screenHeight/2 + 20) {
                        z = f.cells.lenth;
                        if(f.id !== u.id) {
                            return {
                                id: f.id,
                                x: f.x,
                                y: f.y,
                                cells: f.cells,
                                mass_total: Math.round(f.mass_total),
                                hue: f.hue,
                                name: f.name
                            };
                        } else {
                            //console.log("Nombre: " + f.name + " Es Usuario");
                            return {
                                x: f.x,
                                y: f.y,
                                cells: f.cells,
                                mass_total: Math.round(f.mass_total),
                                hue: f.hue,
                            };
                        }
                    }
                }
            })
            .filter(function(f) { return f; });

        sockets[u.id].emit('serverTellPlayerMove', visibleCells, visibleFood, visibleMass, visibleVirus);
        if (leaderboardChanged) {
            sockets[u.id].emit('leaderboard', {
                players: users.length,
                leaderboard: leaderboard
            });
        }
    });
    leaderboardChanged = false;
}

setInterval(move_loop, 1000 / 60);
setInterval(game_loop, 1000);
setInterval(sendUpdates, 1000 / Config.Game.networkUpdateFactor);

// Don't touch, IP configurations.
var ipaddress = process.env.OPENSHIFT_NODEJS_IP || process.env.IP || Config.Game.host;
var serverport = process.env.OPENSHIFT_NODEJS_PORT || process.env.PORT || Config.Game.port;
http.listen( serverport, ipaddress, function() {
    console.log('[DEBUG] Listening on ' + ipaddress + ':' + serverport);
});
