#!/usr/bin/env ruby

=begin

convert_coordinates.rb

This script reads a CSV file with coordinates, converts each position into
a position relative to the first measurement from that source, and outputs
the positions.

=end

class Point
    attr_accessor :x, :y, :z
    def initialize(x, y, z)
        @x = x
        @y = y
        @z = z
    end

    # Subtracts two points
    def - (other)
        Point.new(@x - other.x, @y - other.y, @z - other.z)
    end

    def to_s
        "#{@x},#{@y},#{@z}"
    end
end

def main

    # Track the first recorded position from each source
    first_positions = {}

    input_lines = ARGF.each_line
    # Skip and write headers
    puts input_lines.next

    input_lines.each do |line|
        parts = line.split ','
        if parts.length != 5
            raise RuntimeError("Failed to parse line \"#{line}\"")
        end
        source = parts[0]
        x = parts[1].to_f
        y = parts[2].to_f
        z = parts[3].to_f
        time = parts[4]

        position = Point.new(x, y, z)
        first_position = first_positions[source]
        if !first_position
            first_position = position
            first_positions[source] = position
        end
        position = position - first_position

        puts "#{source},#{position},#{time}"
    end
end

main
