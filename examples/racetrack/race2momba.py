# -*- coding:utf-8 -*-
#
# Copyright (C) 2019, Michaela Klauck <klauck@cs.uni-saarland.de>

from __future__ import annotations

import typing as t

import argparse
import itertools
import pathlib
import re

from momba import model
from momba.ext import jani
from momba.model import expressions, types
from momba.model.expressions import minimum, maximum


parser = argparse.ArgumentParser(description='Reads a track file.')
parser.add_argument('track', type=pathlib.Path, help='the map description in ASCII track format')
parser.add_argument('output', type=pathlib.Path, help='JANI output file')
parser.add_argument('max_speed', type=int, default=3, help='maximal speed of the car')
parser.add_argument('max_acc', type=int, default=3, help='maximal acceleration in one step')
parser.add_argument('--indent', type=int, default=2, help='indentation for JANI file')
parser.add_argument(
    '--allow-momba-operators',
    default=False,
    action='store_true',
    help='use JANI extension x-momba-operators'
)


def main(arguments: t.Optional[t.Sequence[str]] = None) -> None:
    namespace = parser.parse_args(arguments)
    undergrounds = ['tarmac', 'ice', 'sand']

    for car_max_speed in range(namespace.max_speed):
        for car_max_acc in range(namespace.max_acc):
            for underground in undergrounds:
                network = build_model(namespace.track, car_max_speed, car_max_acc, underground)

                out = namespace.output+'_'+car_max_speed+'_'+'_'+car_max_acc+'_'+underground

                out.write_bytes(
                    jani.dump_model(
                        network,
                        indent=namespace.indent,
                        allow_momba_operators=namespace.allow_momba_operators
                    )
                )
    print("done")


def build_model(
    track_path: pathlib.Path,
    max_speed: int,
    max_acc: int,
    underground: str
    ) -> model.Network:
    with track_path.open('r', encoding='utf-8') as track_file:
        firstline = track_file.readline()
        track = track_file.read().replace('\n', '').strip()

    dimension = re.match(r'dim: (?P<width>\d+) (?P<height>\d+)', firstline)
    assert dimension is not None, 'invalid format: dimension missing'

    width, height = int(dimension['width']), int(dimension['height'])
    assert len(track) == width * height, 'given track dimensions do not match actual track size'

    track_blank = [match.start() for match in re.finditer(r'\.', track)]
    track_blocked = [match.start() for match in re.finditer(r'x', track)]
    track_start = [match.start() for match in re.finditer(r's', track)]
    track_goal = [match.start() for match in re.finditer(r'g', track)]
    assert len(track_start) > 0, 'no start field specified'
    assert len(track_goal) > 0, 'no goal field specified'

    def acc_prob(ground: str) -> model.Expression:
        if(ground == 'tarmac'):
            return expressions.div(7, 8)
        elif(ground == 'sand'):
            return expressions.div(1, 3)
        elif(ground == 'ice'):
            return expressions.div(1, 6)
        else:
            raise NotImplementedError('This underground is not specified')

    def acc_underground(ground: str, x: model.Expression) -> model.Expression:
        if(ground == 'tarmac'):
            return x
        if(ground == 'sand'):
            if x > 0:
                return x-1
            else:
                return x+1
        if(ground == 'ice'):
            return expressions.convert(0)

    network = model.Network(model.ModelType.MDP)

    network.declare_constant('DIM_X', types.INT, width)
    network.declare_constant('DIM_Y', types.INT, height)
    network.declare_constant('TRACK_SIZE', types.INT, width * height)

    DIM_X = expressions.identifier('DIM_X')
    DIM_Y = expressions.identifier('DIM_Y')
    TRACK_SIZE = expressions.identifier('TRACK_SIZE')

    network.declare_variable('car_dx', types.INT)
    network.declare_variable('car_dy', types.INT)
    network.declare_variable('car_pos', types.INT[0, TRACK_SIZE - 1])

    car_dx = expressions.identifier('car_dx')
    car_dy = expressions.identifier('car_dy')
    car_pos = expressions.identifier('car_pos')

    network.restrict_initial = expressions.lor(
        *(expressions.eq(car_pos, expressions.convert(pos)) for pos in track_start)
    )

    car = network.create_automaton(name='car')
    location = car.create_location(initial=True)

    def new_speed(current: model.Expression, change: model.Expression) -> model.Expression:
        return expressions.maximum(expressions.minimum(current + change, max_speed), -max_speed)

    for ax, ay in itertools.product(range(-max_acc, max_acc), repeat=2):
        car.create_edge(
            location,
            destinations={
                model.create_destination(location, assignments={
                    'car_dx': new_speed(car_dx, ax),
                    'car_dy': new_speed(car_dy, ay)
                }, probability=acc_prob(underground)),
                model.create_destination(location, assignments={
                    'car_dx': new_speed(car_dx, acc_underground(underground, ax)),
                    'car_dy': new_speed(car_dy, acc_underground(underground, ay))
                }, probability=1-acc_prob(underground))
            },
            action='step'
        )

    controller = network.create_automaton(name='controller')
    location = controller.create_location(initial=True)

    x_coord = car_pos % DIM_X
    y_coord = car_pos // DIM_X

    def out_of_bounds_x(x: model.Expression) -> model.Expression:
        return (x >= DIM_X) | (x < 0)

    def out_of_bounds_y(y: model.Expression) -> model.Expression:
        return (y >= DIM_Y) | (y < 0)

    def out_of_bounds(x: model.Expression, y: model.Expression) -> model.Expression:
        return out_of_bounds_x(x) | out_of_bounds_y(y)

    offtrack = out_of_bounds(x_coord + car_dx, y_coord + car_dy)

    goal = expressions.lor(
        *(expressions.eq(car_pos, expressions.convert(pos)) for pos in track_goal)
    )

    blocked = expressions.lor(
        *(expressions.eq(car_pos, expressions.convert(pos)) for pos in track_blocked)
    )

    # disjuncts = []

    # for x in range(0, DIM_X):
    #     for y in range(0, DIM_Y):
    #         for dx in range(-max_speed, max_speed+1):
    #             for dy in range(-max_speed, max_speed+1):
    #                 if ((x+dx >= 0) & (x+dx < DIM_X) & (y+dy >= 0) & (y+dy < DIM_Y)):
    #                     if(checkcollision(x, y, dx, dy, track, DIM_Y)):
    #                         disj = expressions.land(
    #                             expressions.eq(car_pos, expressions.convert(x+DIM_Y*y)),
    #                             expressions.eq(car_dx, expressions.convert(dx)),
    #                             expressions.eq(car_dy, expressions.convert(dy)))
    #                         disjuncts.append(disj)
    # crashed = expressions.lor(disjuncts)

    def is_blocked_at(pos: model.Expression) -> model.Expression:
        raise NotImplementedError()

    # used floor instead of round sometimes because JANI only knows floor and ceil
    car_will_crash = expressions.lor(
        *(is_blocked_at(
            expressions.floor(
                expressions.mod(car_pos, DIM_Y)
                +(expressions.convert(i)/expressions.convert(max_speed))*car_dx)
            + DIM_Y*expressions.floor(expressions.floor(car_pos/DIM_Y)+(i/max_speed)*car_dy))
            for i in range(max_speed))
    )

    not_terminated = ~goal & ~offtrack & ~car_will_crash

    controller.create_edge(
            location,
            destinations={
                model.create_destination(location, assignments={
                    'car_pos':  maximum(
                        minimum(
                            maximum(minimum(x_coord + car_dx, DIM_X - 1), 0)
                            + DIM_X * maximum(minimum(y_coord + car_dy, DIM_Y - 1), 0),
                            TRACK_SIZE - 1
                        ), 0
                    )
                })
            },
            action='step',
            guard=not_terminated
    )

    car_instance = car.create_instance()
    controller_instance = controller.create_instance()

    composition = network.create_composition(
        {car_instance, controller_instance}
    )
    composition.create_synchronization(
        {
            car_instance: 'step',
            controller_instance: 'step'
        }, result='step'
    )

    return network


if __name__ == '__main__':
    main()
