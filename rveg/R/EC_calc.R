#       Functions to calculate the feature vecture of patterned vegetation as in Mander et al. 2017
#       Patterns should supplied as a binary [0,1] m x n array
#
#       Author: Chris A. Boulton
#       Date: 21th November 2019
#       email: c.a.boulton@exeter.ac.uk
#

#' Function to find the coordinates of pixels neighbouring a pixel at (x,y) in an m*n array.
#' Will return an array of eight coordinates (if including diagonal neighbours) or four if not.
#' @param x The x-coordinate of the pixel of interest
#' @param y The y-coordinate of the pixel of interest
#' @param m The size of the array in x-direction.
#' @param n The size of the array in y-direction.
#' @param diag Include diagonal neighbours if set to TRUE
#' @return Array of neighbouring pixel's x-y coordinates.
#' @export
get_neighbours <- function(x,y,m,n,diag=TRUE) {
    #find indices of surrounding neighbours of point x,y in an m x n array
    #diagonal neighbours also returned as default
    #indices which lie outside of the boundaries are removed
    if (diag == TRUE) {
        neighbours <- array(NA, dim=c(8,2))
        neighbours[1,] <- c(x-1,y+1)
        neighbours[2,] <- c(x,y+1)
        neighbours[3,] <- c(x+1,y+1)
        neighbours[4,] <- c(x-1,y)
        neighbours[5,] <- c(x+1,y)
        neighbours[6,] <- c(x-1,y-1)
        neighbours[7,] <- c(x,y-1)
        neighbours[8,] <- c(x+1,y-1)
    } else {
        neighbours <- array(NA, dim=c(4,2))
        neighbours[1,] <- c(x,y+1)
        neighbours[2,] <- c(x-1,y)
        neighbours[3,] <- c(x+1,y)
        neighbours[4,] <- c(x,y-1)
    }
    if (length(which(neighbours[,1] > m |
                     neighbours[,1] < 1 |
                     neighbours[,2] > n |
                     neighbours[,2] < 1)) > 0) {
        neighbours <- neighbours[-which(neighbours[,1] > m |
                                        neighbours[,1] < 1 |
                                        neighbours[,2] > n |
                                        neighbours[,2] < 1),]
    }
    return(neighbours)
}
#

#' Function that creates a 2-column array of all the edges where neighbour points are both equal to 1
#' @param pattern A 2D binary array
#' @return edges A 2-column array of all edges between signal pixels
#' @export
make_edges <- function(pattern) {

    m <- dim(pattern)[[1]]
    n <- dim(pattern)[[2]]
    edges <- array(0, dim=c(2,2))   #set this up as an array to add to the bottom of and then delete the top two rows at the end
    for (x in 1:m) {
        for (y in 1:n) {
            if (pattern[x,y] == 1) {
                neigh <- NA
                neigh <- get_neighbours(x,y,m,n, diag=TRUE)
                for (i in 1:dim(neigh)[1]) {
                    if (pattern[neigh[i,1],neigh[i,2]] == 1) {
                        edges <- rbind(edges,c((y-1)*m+x,(neigh[i,2]-1)*m+neigh[i,1]))  #trial and error has been used to work out which indices to record
                    }
                }
            }
        }
    }
    edges <- edges[-c(1:2),]
    return(edges)
}

#' Read values from a CSV file into a matrix.
#' @param filename Full path to csv file
#' @return matrix containing 1s and 0s.
#' @export
read_from_csv <- function(filename) {
    df <- utils::read.csv(filename,header=FALSE)
    mat <- as.matrix(df)
    rescaled_mat <- apply(mat, 1:2, function(x){ if (x > 0) return(1) else return(0) })
    return(rescaled_mat)
}

#' Read values from a .png file into a matrix.
#' @param filename Full path to png file
#' @return matrix containing 1s and 0s.
#' @export
read_from_png <- function(filename) {
    image <- png::readPNG(filename)
    rescaled_image <- apply(image, 1:2, function(x){ if (sum(x) > 0) return(0) else return(1)})
    return(rescaled_image)
}


#' Swap zeros and ones in a matrix
#' @param pattern matrix containing 0s and 1s
#' @return matrix containing 1s and 0s.
#' @export
invert_pattern <- function(pattern) {
    inverted_pattern <- apply(pattern, 1:2, function(x){ if (x>0) return(0) else return(1)})
    return(inverted_pattern)
}



#' Function to calculate the Euler Characteristic for a set of graphs corresponding to different subsets
#' of signal pixels in an image.
#' Uses igraph to convert the output from make_edges into a graph object
#' subgraph centrality is then calculated on this
#' as default 5% increments are taken where the highest ranked pixels are used to create a subgraph
#' the number of edges and vertices are then used to calculate the Euler characters as in Mander et al. 2017
#' @param pattern 2D array of 1s and zeros corresponding to a binary image.
#' @param inc size of increment in percentage of pixels (ordered by subgraph centrality) in feature vector.
#' @return EC_vec list of Euler Characteristic values (feature vector).
calc_EC <- function(pattern, inc=5) {

    require('igraph')
    graph_edges <- make_edges(pattern)
    graph <- igraph::graph_from_data_frame(graph_edges, directed = TRUE, vertices = NULL)
    SC <- subgraph_centrality(graph, diag = FALSE)

    pixel_sort <- as.numeric(names(rev(sort(SC))))
    breaks <- round(seq(inc,100,inc)*length(SC)/100)
    EC_vec <- rep(NA, length(breaks))

    for (i in 1:length(breaks)) {
        subgraph_edges <- graph_edges[which(graph_edges[,1] %in% pixel_sort[1:breaks[i]] & graph_edges[,2] %in% pixel_sort[1:breaks[i]]),]
        V <- breaks[i]
        E <- dim(subgraph_edges)[1]/2
        EC_vec[i] <- V - E
    }

    return(EC_vec)
}
