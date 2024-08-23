import Data.Maybe
import Text.Read (readMaybe)

-- Disclaimer: every "bug" in this program is a feature...

main :: IO ()
main = game

------------------------- Sorting

merge :: Ord a => [a] -> [a] -> [a]
merge xs [] = xs
merge [] ys = ys
merge (x:xs) (y:ys)
    | x <  y    = x : merge    xs (y:ys)
    | x == y    = x : merge    xs    ys
    | otherwise = y : merge (x:xs)   ys

-- Sort and remove duplicates.
msort :: Ord a => [a] -> [a]
msort []  = []
msort [x] = [x]
msort xs  = msort (take n xs) `merge` msort (drop n xs)
  where
    n = length xs `div` 2


sortPair :: (Node, Node) -> (Node, Node)
sortPair (p1,p2) = (min p1 p2, max p1 p2)

------------------------- Game world types

type Character = String
type Party     = [Character]

type Node      = Int
type Location  = String
type Map       = [(Node,Node)]

data Game      = Over
               | Game Map Node Party [Party]
  deriving (Eq,Show)

type Event     = Game -> Game


testGame :: Node -> Game
testGame i = Game [(0,1)] i ["Russell"] [[],["Brouwer","Heyting"]]

------------------------- Assignment 1: The game world

connected :: Map -> Node -> [Node]
connected m n = msort [ if n == p1 then p2 else p1 | (p1, p2) <- m, n == p1 || n == p2 ]


twoNodesConnected :: Node -> Node -> Map -> Bool
twoNodesConnected n1 n2 m = n1 `elem` connected m n2


-- `$` basically means "apply the result of the RHS operation to the LHS".
-- It helps to reduce the number of `()` for better readability.
connect :: Node -> Node -> Map -> Map
connect n1 n2 m
    | not (twoNodesConnected n1 n2 m) = msort $ sortPair (n1, n2) : m
    | otherwise                       = m


disconnect :: Node -> Node -> Map -> Map
disconnect n1 n2 m
    | twoNodesConnected n1 n2 m = filter (/= sortPair (n1, n2)) m
    | otherwise                 = m


add :: Party -> Event
add _  Over                              = Over
add p (Game m n playersParty allParties) = Game m n (msort (p ++ playersParty)) allParties


addAt :: Node -> Party -> Event
addAt _     _             Over                              = Over
addAt _     []           (Game m n playersParty allParties) = Game m n playersParty allParties
addAt iNode (char:chars) (Game m n playersParty allParties) = addAt iNode chars (Game m n playersParty (addToParty iNode char allParties))
    where addToParty iNode char allParties = [
                                               if i == iNode
                                               then msort (char:gameParty)
                                               else gameParty
                                               | (i, gameParty) <- zip [0..] allParties
                                             ]

-- The `@` is an "as-pattern". It allows to keep a
-- reference to the entire pattern-matched value.
addHere :: Party -> Event
addHere _       Over          = Over
addHere p game@(Game _ n _ _) = addAt n p game


removeCharacters :: Party -> Party -> Party
removeCharacters charsToRemove chars = msort [ char | char <- chars, notElem char charsToRemove]


remove :: Party -> Event
remove _  Over                              = Over
remove p (Game m n playersParty allParties) = Game m n (removeCharacters p playersParty) allParties


removeAt :: Node -> Party -> Event
removeAt _     _      Over                              = Over
removeAt iNode chars (Game m n playersParty allParties) = Game m n playersParty (removeFromParty iNode chars allParties)
    where removeFromParty iNode chars allParties = [
                                                     if i == iNode
                                                     then removeCharacters chars gameParty
                                                     else gameParty
                                                     | (i, gameParty) <- zip [0..] allParties
                                                   ]


removeHere :: Party -> Event
removeHere _       Over          = Over
removeHere p game@(Game _ n _ _) = removeAt n p game

------------------------- Assignment 2: Dialogues

data Dialogue = Action  String Event
              | Branch  (Game -> Bool) Dialogue Dialogue
              | Choice  String [( String, Dialogue )]


testDialogue :: Dialogue
testDialogue = Branch ( isAtZero )  -- Branch condition to choose the dialogue.
    -- 1st dialogue branch.
    ( Choice "Russell: Let's get our team together and head to Error." [] )
    -- 2nd dialogue branch.
    (
        Choice "Brouwer: How can  help you?"
        [
            -- 1st choice.
            ( "Could  get a haircut?", Choice "Brouwer: Of course." [] ),
            -- 2nd choice.
            (
                "Could  get a pint?", Choice "Brouwer: Of course. Which would you like?"
                    [ ("The Segmalt.", Action "" id), ("The Null Pinter.", Action "" id) ]
            ),
            -- 3rd choice.
            ( "Will you join us on a dangerous adventure?", Action "Brouwer: Of course." (add ["Brouwer"] . removeHere ["Brouwer"]) )
        ]
    )
    where isAtZero (Game _ n _ _) = n == 0


-- NOTE: the auxiliary functions are defined before they 
-- are used, similarly to how they would be ordered in C.


formatDisplayedOpt :: Int -> String -> String
formatDisplayedOpt i str = "  " ++ show (i) ++ "." ++ " " ++ str


-- The prompt appears in multiple places, therefore make it
-- into a function to be able to easily change in the future.
displayPrompt :: IO ()
displayPrompt = putStr ">> "


displayInpError :: IO ()
displayInpError = do
    putStrLn "You shall not pass! (invalid input)"
    putStrLn ""


dialogue :: Game -> Dialogue -> IO Game
-- This case is not mentioned in the spec, added for robustness.
dialogue Over _ = do
    -- Print "Game Over"
    putStr "Game "
    return Over

-- Action case.
dialogue game (Action str event) = do
    putStrLn (str)
    return (event game)

-- Branch case.
dialogue game (Branch conditionMet d1 d2) = do
    if conditionMet game then
        dialogue game d1
    else
        dialogue game d2

-- Choice cases.
dialogue game (Choice str []) = do
    putStrLn str
    return game

dialogue game choice@(Choice choiceStr choices) = do
    putStrLn choiceStr
    displayDialogueOpts game choice 1
    displayPrompt

    inp <- getLine
    let intInp = readMaybe inp :: Maybe Int

    -- `case <expr> of` is used for pattern matching inside a function.
    case intInp of
        Nothing -> handleInvalidInp game choice
        Just intInp -> processChoice intInp
    
    where
        -- Where `Int` is the number of the option in the displayed list.
        displayDialogueOpts :: Game -> Dialogue -> Int -> IO ()
        displayDialogueOpts _    (Choice _         ((str, _): [] )) i = putStrLn (formatDisplayedOpt i str)
        displayDialogueOpts game (Choice choiceStr ((str, _):opts)) i = do
            putStrLn (formatDisplayedOpt i str)
            displayDialogueOpts game (Choice choiceStr opts) (i+1)

        handleInvalidInp :: Game -> Dialogue -> IO Game
        handleInvalidInp game dial = do
            displayInpError
            dialogue game dial

        continueDialogue :: (String, Dialogue) -> IO Game
        continueDialogue (responseStr, responseDialogue) = do
            putStrLn ""
            dialogue game responseDialogue

        processChoice :: Int -> IO Game
        processChoice intInp
            | outOfBounds = handleInvalidInp game choice
            | intInp == 0 = do { putStrLn ""; return game }  -- Exit the dialogue if 0 is entered.
            | otherwise   = continueDialogue $ choices !! (intInp - 1)
            where outOfBounds = (intInp < 0) || (intInp > length choices)


-- `fromMaybe <defaultValueIfNothing> <JustValue>` returns `<value>`.
findDialogue :: Party -> Dialogue
findDialogue inpP = fromMaybe (Action "There is nothing we can do." id) maybeFoundDialogue
    -- `listToMaybe :: [a] -> Maybe a`.
    where maybeFoundDialogue = listToMaybe [ dialogue | (givenP, dialogue) <- theDialogues, givenP == inpP ]

------------------------- Assignment 3: The game loop

-- More descriptive than `Either`.
data LocOrChr = Loc Node | Chr Character

-- This and `processUsersInpStep` functions are only used inside `step`,
-- however they aren't in its `where` clause for better readability.
displayMenu :: Game -> IO ()
displayMenu game@(Game m n playersParty allParties) = do

    displayCurLocation n
    i <- displayTravelLocs m n
    nextI <- displayPlayersParty playersParty i
    displayCurLocParty n allParties nextI

    where
        displayCurLocation :: Node -> IO ()
        displayCurLocation curLoc = do
            putStr "You are in "
            putStrLn (theDescriptions !! curLoc)

        displayTravelLocs :: Map -> Node -> IO Int
        displayTravelLocs m curLoc = do

            let locs = connected m curLoc
            let toBePrinted = [ putStrLn $ formatDisplayedOpt i (theLocations !! locI) | (i, locI) <- zip [1..] locs ]

            if (length toBePrinted) /= 0 then do
                putStrLn "You can travel to:"
                -- Print every `putStrLn` in the list.
                sequence_ toBePrinted
                let nextI = (length locs) + 1
                return nextI

            else do
                putStrLn "Your left toe hurts, you can't travel anywhere."
                return 1

        getCharsToDisplay :: Party -> Int -> [ IO () ]
        getCharsToDisplay p i = [ putStrLn (formatDisplayedOpt i char) | (i, char) <- zip [i..] p ]

        displayPlayersParty :: Party -> Int -> IO Int
        displayPlayersParty p i = do
            let chars = getCharsToDisplay p i

            if (length chars) > 0 then do
                putStrLn "With you are: "
                sequence_ chars
            else 
                putStrLn "No man is an island, except for you (you're travelling alone)."

            let nextI = i + (length p)
            return nextI

        displayCurLocParty :: Node -> [Party] -> Int -> IO ()
        displayCurLocParty curLoc allParties i = do
            let p = allParties !! curLoc
            let chars = getCharsToDisplay p i

            if (length chars) > 0 then do
                putStrLn "You can see: "
                sequence_ chars
            else do
                putStrLn "After hours of coding, it's like the world outside has vanished."
                putStrLn "You can't see anybody else around."


processUsersInpStep :: [Maybe Int] -> Game -> IO Game
processUsersInpStep maybeIntsInp game@(Game m n playersParty allParties) = do

    let inpIsEmpty = (length maybeIntsInp == 0)
    let inpIsNotInt = Nothing `elem` maybeIntsInp

    if inpIsEmpty || inpIsNotInt then
        handleInvalidInp

    else do
        -- A single list of either Locations, Characters or both. The order of
        -- elements corresponds to the order of options displayed to the user.
        let opts = map Loc (connected m n) ++ map Chr playersParty ++ map Chr (allParties !! n)
        -- Convert, sort and remove duplicates to make make an "auto-correction"
        -- system, e.g. turn input "5 3 3 4" into "3 4 5".
        let intsInp = msort $ map (\(Just int) -> int) maybeIntsInp
        let iOutOfRange = (head intsInp < 0) || (last intsInp > length opts)

        if iOutOfRange then do
            handleInvalidInp

        -- Entering 0 ends the game immediately (if not in a dialogue).
        else if intsInp == [0] then
            step Over

        else do
            -- Descriptively naming the variables instead of commenting 
            -- everything for better clarity and readability.
            let inpOpts = [ opt | (optI, opt) <- zip [1..] opts, i <- intsInp, optI == i ]
            let containsBothLocsAndChars = (any isLoc inpOpts) && (any isChr inpOpts)
            let containsMultipleLocs = (all isLoc inpOpts) && (length inpOpts > 1)
            if containsBothLocsAndChars || containsMultipleLocs then do
                handleInvalidInp
            else
                handleValidInp inpOpts

    where
        handleInvalidInp :: IO Game
        handleInvalidInp = do
            displayInpError
            step game

        isLoc :: LocOrChr -> Bool
        isLoc (Loc _) = True
        isLoc _       = False

        isChr :: LocOrChr -> Bool
        isChr (Chr _) = True
        isChr _       = False

        handleValidInp :: [LocOrChr] -> IO Game
        -- Go to a single location.
        handleValidInp (Loc newLoc:[]) = return (Game m newLoc playersParty allParties)
        -- Talk to multiple characters.
        handleValidInp chrs@(Chr _:_) = do
            let party = msort $ map (\(Chr chr) -> chr) chrs
            dialogue game (findDialogue party)
        -- Catch all unexpected cases, if any.
        handleValidInp _ = return game


step :: Game -> IO Game
step       Over          = return Over
step game@(Game _ _ _ _) = do

    displayMenu game
    displayPrompt

    inp <- getLine
    let maybeInp = map readMaybe (words inp) :: [Maybe Int]

    putStrLn ""
    processUsersInpStep maybeInp game 


game :: IO ()
game = do
    startState <- step start
    loop startState
    where
        loop s = do
            newState <- step s
            case newState of
                game@(Game _ _ _ _) -> loop game
                Over                -> putStrLn "GAME OVER!"

------------------------- Assignment 4: Safety upgrades
-- Safety upgrades have been implemented in assignments 2 and 3.

------------------------- Assignment 5: Solving the game

data Command  = Travel [Int] | Select Party | Talk [Int]
  deriving Show

type Solution = [Command]

talk :: Game -> Dialogue -> [(Game, [Int])]
talk Over _        = []
talk game dialogue = traverse game dialogue []
  where
    -- Traverse and accumulate the choices (in reverse order) until `Action` is reached.
    traverse :: Game -> Dialogue -> [Int] -> [(Game, [Int])]
    traverse game (Branch conditionMet d1 d2) accum 
        | conditionMet game = traverse game d1 accum 
        | otherwise         = traverse game d2 accum

    traverse game (Choice _ choices) accum = 
        concat [ traverse game d (i:accum) | (i, (_, d)) <- zip [1..] choices ]

    traverse game (Action _ event) accum = [(event game, reverse accum)]


-- `select` is just the power set.
select :: Game -> [Party]
select  Over                              = []
select (Game _ n playersParty allParties) = msort $ foldl (\accum char -> accum ++ map (char:) accum) [[]] chars
    where chars = playersParty ++ (allParties !! n)


-- Nooo, thanks.
travel :: Map -> Node -> [(Node,[Int])]
travel = undefined

allSteps :: Game -> [(Solution,Game)]
allSteps = undefined

solve :: Game -> Solution
solve = undefined

walkthrough :: IO ()
walkthrough = (putStrLn . unlines . filter (not . null) . map format . solve) start
  where
    format (Travel []) = ""
    format (Travel xs) = "Travel: " ++ unwords (map show xs)
    format (Select xs) = "Select: " ++ foldr1 (\x y -> x ++ ", " ++ y) xs
    format (Talk   []) = ""
    format (Talk   xs) = "Talk:   " ++ unwords (map show xs)


------------------------- Game data

start :: Game
start = Game theMap 0 [] theCharacters

theMap :: Map
theMap = [(1,2),(1,6),(2,4)]

theLocations :: [Location]
theLocations =
  -- Logicester
  [ "Home"           -- 0
  , "Brewpub"        -- 1
  , "Hotel"          -- 2
  , "Hotel room n+1" -- 3
  , "Temple"         -- 4
  , "Back of temple" -- 5
  , "Takeaway"       -- 6
  , "The I-50"       -- 7
  ]

theDescriptions :: [String]
theDescriptions =
  [ "your own home. It is very cosy."
  , "the `Non Tertium Non Datur' Brewpub & Barber's."
  , "the famous Logicester Hilbert Hotel & Resort."
  , "front of Room n+1 in the Hilbert Hotel & Resort. You knock."
  , "the Temple of Linearity, Logicester's most famous landmark, designed by Le Computier."
  , "the back yard of the temple. You see nothing but a giant pile of waste paper."
  , "Curry's Indian Takeaway, on the outskirts of Logicester."
  , "a car on the I-50 between Logicester and Computerborough. The road is blocked by a large, threatening mob."
  ]

theCharacters :: [Party]
theCharacters =
  [ ["Bertrand Russell"]                    -- 0  Home
  , ["Arend Heyting","Luitzen Brouwer"]     -- 1  Brewpub
  , ["David Hilbert"]                       -- 2  Hotel
  , ["William Howard"]                      -- 3  Hotel room n+1
  , ["Jean-Yves Girard"]                    -- 4  Temple
  , []                                      -- 5  Back of temple
  , ["Haskell Curry", "Jean-Louis Krivine"] -- 6  Curry's takeaway
  , ["Gottlob Frege"]                       -- 7  I-50
  ]

theDialogues :: [(Party,Dialogue)]
theDialogues = let
  always _ = True
  end str  = Choice str []
  isconn  _ _  Over           = False
  isconn  i j (Game m _ _ _ ) = elem i (connected m j)
  here         Over           = 0
  here        (Game _ n _ _ ) = n
  inParty   _  Over           = False
  inParty   c (Game _ _ p _ ) = elem c p
  isAt    _ _  Over           = False
  isAt    n c (Game _ _ _ ps) = elem c (ps !! n)
  updateMap _  Over           = Over
  updateMap f (Game m n p ps) = Game (f m) n p ps
 in
  [ ( ["Russell"] , Choice "Russell: Let's go on an adventure!"
      [ ("Sure." , end "You pack your bags and go with Russell.")
      , ("Maybe later.", end "Russell looks disappointed.")
      ]
    )
  , ( ["Heyting","Russell"] , end "Heyting: Hi Russell, what are you drinking?\nRussell: The strong stuff, as usual." )
  , ( ["Bertrand Russell"] , Branch (isAt 0 "Bertrand Russell") ( let
      intro = "A tall, slender, robed character approaches your home. When he gets closer, you recognise him as Bertrand Russell, an old friend you haven't seen in ages. You invite him in.\n\nRussell: I am here with a important message. The future of Excluded-Middle Earth hangs in the balance. The dark forces of the Imperator are stirring, and this time, they might not be contained.\n\nDo you recall the artefact you recovered in your quest in the forsaken land of Error? The Loop, the One Loop, the Loop of Power? It must be destroyed. I need you to bring together a team of our finest Logicians, to travel deep into Error and cast the Loop into lake Bottom. It is the only way to terminate it."
      re1   = ("What is the power of the Loop?" , Choice "Russell: for you, if you put it on, you become referentially transparent. For the Imperator, there is no end to its power. If he gets it in his possession, he will vanquish us all." [re2])
      re2   = ("Let's go!" , Action "Let's put our team together and head for Error." (updateMap (connect 1 0) . add ["Bertrand Russell"] . removeHere ["Bertrand Russell"]) )
      in Choice intro [re1,re2]
      ) ( Branch ( (==7).here) (end "Russell: Let me speak to him and Brouwer."
      ) (end "Russell: We should put our team together and head for Error." ) )
    )
  , ( ["Arend Heyting"] , Choice "Heyting: What can I get you?"
      [ ( "A pint of Ex Falso Quodbibet, please." , end "There you go." )
      , ( "The Hop Erat Demonstrandum, please."   , end "Excellent choice." )
      , ( "Could I get a Maltus Ponens?"          , end "Mind, that's a strong one." )
      ]
    )
  , ( ["Luitzen Brouwer"] , Branch (isAt 1 "Luitzen Brouwer")
      ( Choice "Brouwer: Haircut?"
        [ ( "Please." , let
          intro = "Brouwer is done and holds up the mirror. You notice that one hair is standing up straight."
          r1 i  = ( "There's just this one hair sticking up. Could you comb it flat, please?" , d i)
          r2    = ( "Thanks, it looks great." , end "Brouwer: You're welcome.")
          d  i  | i == 0    = Choice intro [r2]
                | otherwise = Choice intro [r1 (i-1),r2]
        in d 100)
        , ( "Actually, could you do a close shave?" , end "Of course. I shave everyone who doesn't shave themselves." )
        , ( "I'm really looking for help." , Choice "Brouwer: Hmmm. What with? Is it mysterious?"
          [ ( "Ooh yes, very. And dangerous." , Action "Brouwer: I'm in!" (add ["Luitzen Brouwer"] . removeHere ["Luitzen Brouwer"]) )
          ] )
        ]
      )
      ( end "Nothing" )
    )
  , ( ["David Hilbert"] , Branch (not . isconn 2 3) (let
        intro = "You wait your turn in the queue. The host, David Hilbert, puts up the first guest in Room 1, and points the way to the stairs.\n\nYou seem to hear that the next couple are also put up in Room 1. You decide you must have misheard. It is your turn next.\n\nHilbert: Lodging and breakfast? Room 1 is free."
        re1   = ("Didn't you put up the previous guests in Room 1, too?" , Choice "Hilbert: I did. But everyone will move up one room to make room for you if necessary. There is always room at the Hilbert Hotel & Resort." [("But what about the last room? Where do the guests in the last room go?" , Choice "Hilbert: There is no last room. There are always more rooms." [("How can there be infinite rooms? Is the hotel infinitely long?" , Choice "Hilbert: No, of course not! It was designed by the famous architect Zeno Hadid. Every next room is half the size of the previous." [re2])])])
        re2   =  ("Actually, I am looking for someone." , Action "Hilbert: Yes, someone is staying here. You'll find them in Room n+1. Through the doors over there, up the stairs, then left." (updateMap (connect 2 3)))
      in Choice intro [re1,re2]
      ) (end "Hilbert seems busy. You hear him muttering to himself: Problems, problems, nothing but problems. You decide he has enough on his plate and leave." )
    )
  , ( ["William Howard"] ,  Branch (isAt 3 "William Howard")
      (Choice "Howard: Yes? Are we moving up again?" [("Quick, we need your help. We need to travel to Error." , Action "Howard: Fine. My bags are packed anyway, and this room is tiny. Let's go!" (add ["William Howard"] . removeAt 3 ["William Howard"]))]
      ) (Branch (isAt 6 "William Howard") (Choice "Howard: What can I get you?"
        [ ("The Lambda Rogan Josh with the Raita Monad for starter, please." , end "Coming right up.")
        , ("The Vindaloop with NaN bread on the side." , Choice "Howard: It's quite spicy." [("I can handle it." , end "Excellent." ) ] )
        , ("The Chicken Booleani with a stack of poppadums, please.", end "Good choice." )
        ]
      ) (end "Howard: We need to find Curry. He'll know the way.")
    ) )
  , ( ["Jean-Yves Girard"] , Branch (isconn 4 5)  (end "You have seen enough here.") (Action "Raised on a large platform in the centre of the temple, Girard is preaching the Linearity Gospel. He seems in some sort of trance, so it is hard to make sense of, but you do pick up some interesting snippets. `Never Throw Anything Away' - you gather they must be environmentalists - `We Will Solve Church's Problems', `Only This Place Matters'... Perhaps, while he is speaking, now is a good time to take a peek behind the temple..." (updateMap (connect 4 5) ))
    )
  , ( ["Vending machine"] , Choice "The walls of the Temple of Linearity are lined with vending machines. Your curiosity gets the better of you, and you inspect one up close. It sells the following items:"
      [ ( "Broccoli"  , end "You don't like broccoli." )
      , ( "Mustard"   , end "It might go with the broccoli." )
      , ( "Watches"   , end "They seem to have a waterproof storage compartment. Strange." )
      , ( "Camels"    , end "You don't smoke, but if you did..." )
      , ( "Gauloises" , end "You don't smoke, but if you did..." )
      ]
    )
  , ( ["Jean-Louis Krivine"] , end "Looking through the open kitchen door, you see the chef doing the dishes. He is rinsing and stacking plates, but it's not a very quick job because he only has one stack. You also notice he never passes any plates to the front. On second thought, that makes sense - it's a takeaway, after all, and everything is packed in cardboard boxes. He seems very busy, so you decide to leave him alone."
    )
  , ( ["Haskell Curry"] , Branch (isAt 6 "Haskell Curry")
      (Choice "Curry: What can I get you?"
        [ ("The Lambda Rogan Josh with the Raita Monad for starter, please." , end "Coming right up.")
        , ("The Vindaloop with NaN bread on the side." , Choice "Curry: It's quite spicy." [("I can handle it." , end "Excellent." ) ] )
        , ("The Chicken Booleani with a stack of poppadums, please.", end "Good choice." )
        , ("Actually, I am looking for help getting to Error." , end "Curry: Hmm. I may be able to help, but I'll need to speak to William Howard.")
        ]
      ) (end "Nothing")
    )
  , ( ["Haskell Curry","William Howard"] , Branch (not . isconn 6 7) (Action "Curry:  You know the way to Error, right?\nHoward: I thought you did?\nCurry:  Not really. Do we go via Computerborough?\nHoward: Yes, I think so. Is that along the I-50?\nCurry:  Yes, third exit. Shall I go with them?\nHoward: sure. I can watch the shop while you're away." (add ["Haskell Curry"] . removeAt 6 ["Haskell Curry"] . addAt 6 ["William Howard"] . remove ["William Howard"] . updateMap (connect 6 7) )) (end "It's easy, just take the third exit on I-50.")
    )
  , ( ["Gottlob Frege"] , end "A person who appears to be the leader of the mob approaches your vehicle. When he gets closer, you recognise him as Gottlob Frege. You start backing away, and he starts yelling at you.\n\nFrege: Give us the Loop! We can control it! We can wield its power!\n\nYou don't see a way forward. Perhaps Russell has a plan." )
  , ( ["Bertrand Russell","Gottlob Frege","Luitzen Brouwer"] , let
        intro = "Frege is getting closer, yelling at you to hand over the Loop, with the mob on his heels, slowly surrounding you. The tension in the car is mounting. But Russell calmly steps out to confront Frege.\n\nRussell:"
        re1   = ( "You cannot control its power! Even the very wise cannot see all ends!" , Choice "Frege: I can and I will! The power is mine!\n\nRussell:" [re2,re3] )
        re2   = ( "Brouwer, whom do you shave?" , Choice "Brouwer: Those who do not shave themselves. Obviously. Why?\n\nRussell:" [re3] )
        re3   = ( "Frege, answer me this: DOES BROUWER SHAVE HIMSELF?" , Action
                  "Frege opens his mouth to shout a reply. But no sound passes his lips. His eyes open wide in a look of bewilderment. Then he looks at the ground, and starts walking in circles, muttering to himself and looking anxiously at Russell. The mob is temporarily distracted by the display, uncertain what is happening to their leader, but slowly enclosing both Frege and Russell. Out of the chaos, Russell shouts:\n\nDRIVE, YOU FOOLS!\n\nYou floor it, and with screeching tires you manage to circle around the mob. You have made it across.\n\nEND OF ACT 1. To be continued..."
                  (const Over)
                )
      in Choice intro [re1,re2,re3]
    )
  , ( ["Bertrand Russell","Haskell Curry","Luitzen Brouwer"] , Branch ((==7).here) (end "Road trip! Road trip! Road trip!") (end "Let's head for Error!")
    )
  ]

